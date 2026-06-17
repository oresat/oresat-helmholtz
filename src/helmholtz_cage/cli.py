"""
Command Line Interface module
Handles incoming serial commands
"""

import select
import sys

from micropython import const

HISTORY_MAX_SIZE = const(40)
STDIN_POLL_TIMEOUT_MS = const(100)


class Symbol(str):  # noqa: SLOT000
    pass


eof_object = Symbol('#<eof-object>')  # Note: uninterned; can't be read


class Command:
    """
    General CLI command class
    Usage:
    def sum_3_numbers(a: int, b: int, c: int):
        sum = a + b + c
        return f"{sum}\n"
    sum = Command(
    "sum",
    sum_3_numbers,
    [a],
    [(("-b", "-bravo"), int), (("-c",), int)],
    "Add two numbers and print the result"
    )
    cli.register_command(sum)
    > sum -a 1 -b 2
    """

    def __init__(self, name, callback, argspec, default_args, help_text):
        self.name = name  # name of the command, eg "help", "exit", "clear"
        self.callback = callback  # function to be called in response to the command
        # Default args are any non user provided args to be passed to the callback
        # When writing a callback, defaults arguments MUST come before user args in the signature
        self.default_args = default_args
        # The argspec is a list of args to be passed to the callback, in order(!), and their types.
        # For each entry to the list, the first item is a tuple of any length containing all the
        # inputs that arg will match against. The arg name must begin with a '-'.
        # The second item is the type the arg will be cast to
        self.argspec = argspec
        self.help_text = help_text  # what gets printed when the user inputs 'help'


class ParserError(Exception):
    pass


class Cli:
    """
    Command line interface class.
    Contains methods to manage history, register, parse, and evaluate incoming commmands,
    as well as dispatch their associated callbacks.
    """

    def __init__(self, prompt):
        self.history = []  # buffer to hold previous commands
        self.commands = {}  # registry of commands, key is the name, value is the Commmand object
        self.prompt = prompt
        self.line = ''
        self.index = 0
        self.history_offset = -1
        self.user_input = ''
        self.poller = select.poll()
        self.poller.register(sys.stdin, select.POLLIN)

        self.register_commands(
            [
                Command(
                    name="clear",
                    callback=None,
                    default_args=None,
                    argspec=None,
                    help_text="Clear the terminal",
                ),
                Command(
                    name="help",
                    callback=self.get_help_texts,
                    default_args=None,
                    argspec=None,
                    help_text="Display this message",
                ),
                Command(
                    name="exit",
                    callback=None,
                    default_args=None,
                    argspec=None,
                    help_text="Exit the repl",
                ),
            ]
        )

        sys.stdout.write(self.prompt)

    def redraw_prompt(self):
        sys.stdout.write(f"\n{self.prompt}")

    def add_to_history(self, line):
        """
        Add a command to the history buffer
        """
        if line and (not self.history or self.history[0] != line):
            self.history = self.history[: HISTORY_MAX_SIZE - 1]
            self.history.insert(0, line.strip())

    def get_history(self, offset):
        """
        Return a command from the history buffer
        """
        if offset < 0 or offset >= len(self.history):
            return ''
        return self.history[offset]

    def get_help_texts(self):
        """
        Return a string of all the registered commands' help texts and args
        """
        txts = ""

        names = list(self.commands.keys())
        names.sort()  # sort help text entries alphabetically

        for cmd_name in names:
            cmd = self.commands[cmd_name]
            txts += f"{cmd_name}: {cmd.help_text}\n"
            if cmd.argspec:
                for arg in cmd.argspec:  # for name, cmd in self.commands.items():
                    txts += f"{' ' * 4}{list(arg[0])!s}: {arg[1].__name__!s}\n"

        return txts

    def register_command(self, command):
        """
        Register a command to the CLI's inner registry
        """
        LOGGER.debug("registering command: '%s' with args: %s", command.name, str(command.argspec))
        self.commands.update({command.name: command})

    def register_commands(self, commands):
        for command in commands:
            self.register_command(command)

    def parse(self, x):
        """
        Parse and validate the incoming input into a dict.
        The first entry to the dict is the name of the command.
        The second entry is an ordered list of the args to be passed to the callback.
        """
        if len(x) < 1:
            return None

        chunks = x.split()  # split input by whitespace into list

        if chunks[0] not in self.commands:
            raise ParserError("Command not recognized")

        cmd = self.commands[chunks[0]]  # first chunk should be the name of the command

        if len(chunks) < 2 and cmd.argspec is not None:
            raise ParserError(f"'{cmd.name}' requires arguments that weren't provided")

        if not cmd.argspec:
            # Ignore extraneous args
            return {"name": cmd.name, "args": None}

        raw_args = chunks[1:]  # remaining chunks should be the args

        flags = list(filter(lambda x: x[0] == "-", raw_args))

        if len(flags) < len(cmd.argspec):
            raise ParserError(f"Command '{cmd.name}' requires arguments that weren't provided")

        parsed_args = []

        for i, arg in enumerate(raw_args):
            if arg[0] == '-':
                try:
                    # check if the next value passed to the flag is also a flag, which isn't allowed
                    next_arg = raw_args[i + 1]
                    if next_arg[0] == "-":
                        raise ParserError(f"Unexpected value '{next_arg}' passed to flag '{arg}'")
                except IndexError as e:
                    # nothing else was passed after the flag, which is also an error
                    raise ParserError(f"No value passed to arg '{arg}' for '{cmd.name}'") from e

                match = None
                for pos, argspec in enumerate(cmd.argspec):
                    # validate the incoming arg against the argspec,
                    # and store its position for later ordering
                    if arg in argspec[0]:
                        match = (pos, argspec)
                        break
                if not match:
                    raise ParserError(f"Unexpected argument '{arg}' passed to '{cmd.name}'")
                try:
                    pos = match[0]
                    # the argspec contains the proper data type for the arg. Use it to cast the arg
                    cast_arg = match[1][1](
                        raw_args[i + 1].strip("'\"")
                    )  # the next chunk should be the data
                    parsed_args.append((pos, cast_arg))
                except Exception as e:
                    raise ParserError(f"Error parsing '{raw_args[i + 1]}' - {e}") from e

        # these args may be out of order, so use the argspecs ordering to be sure
        # when they are passed to the callback they are positioned properly
        ordererd_args = [0] * len(parsed_args)
        for arg in parsed_args:
            ordererd_args[arg[0]] = arg[1]

        return {"name": cmd.name, "args": ordererd_args}

    def evaluate(self, parsed_input):
        """
        Evaluate the parsed data, dispatching the proper callback
        and returning the response string.
        """
        try:
            cmd_name = parsed_input["name"]
            args = parsed_input["args"]
            cmd = self.commands[cmd_name]
            if parsed_input["name"] == "clear":
                ret = "\033[H\033[2J"  # clear terminal code
            elif parsed_input["name"] == "exit":
                ret = parsed_input["name"]
            elif args and cmd.default_args:
                ret = cmd.callback(*cmd.default_args, *args)
            elif args:
                ret = cmd.callback(*args)
            elif cmd.default_args:
                ret = cmd.callback(*cmd.default_args)
            else:
                ret = cmd.callback()
        except TypeError as e:
            ret = f"Error dispatching {cmd.name} - {e}\n"
        except KeyError as e:
            ret = f"Unexpected input provided to 'evaluate' method - {e}\n"
        return ret

    def process_incoming_bytes(self):
        """
        Checks stdin for incoming bytes and processes them.
        This works similarly to how a repl would. However, instead of using a loop
        this will keep track of the state of the line between calls,
        allowing main to perform other tasks while waiting for bytes to come in.
        Returns a bool that will be true if the user enters 'exit'.
        """
        ch = None

        # Check for bytes coming in from stdin
        for result in self.poller.ipoll(STDIN_POLL_TIMEOUT_MS):
            stdin = result[0]  # first entry is the object we polled
            event = result[1]  # second entry is what happened when we polled it
            if event & select.POLLIN:
                # Bytes have been received
                ch = ord(stdin.read(1))
            elif event & (select.POLLHUP | select.POLLERR):
                # This should never happen, but if it does somehow we should know
                LOGGER.error("Unexpected Error from stdin: %s", str(event))

        if ch is None:
            # No bytes received. Yield to the caller
            return False

        # Bytes received. Process them

        if 32 <= ch <= 126:  # printable character
            self.line = self.line[: self.index] + chr(ch) + self.line[self.index :]
            self.index += 1

        elif ch in {10, 13}:  # EOL - try to process
            self.user_input = (
                self.user_input + ' ' + self.line.strip() if self.user_input else self.line.strip()
            )
            self.add_to_history(self.line.strip())
            self.line = ''
            try:
                try:
                    x = self.parse(self.user_input)
                    if not x:
                        sys.stdout.write('\n')
                        self.user_input = ''
                        return False
                except ParserError as e:
                    sys.stdout.write(f'\n{e}\n')
                    self.user_input = ''
                    return False

                if x is eof_object:
                    raise SyntaxError('unexpected EOF in list')  # noqa: TRY301

                val = self.evaluate(x)

                if val is not None:
                    if val == "exit":
                        return True
                    sys.stdout.write(f'\n{val}')

                self.user_input = ''
                prompt = '... ' if self.user_input else self.prompt
                sys.stdout.write(prompt)
                self.index = 0
                self.line = ''
                self.history_offset = -1

            except SyntaxError as e:
                if str(e) != 'unexpected EOF in list':
                    sys.stdout.write('\n')
                    sys.stdout.write(str(e))
                    self.user_input = ''

        elif ch in {8, 127}:  # backspace/DEL
            if self.index > 0:
                self.line = self.line[: self.index - 1] + self.line[self.index :]
                self.index -= 1

        elif ch == 27:  # ESC
            next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
            if next1 == 91:  # [
                if next2 == 68:  # left arrow
                    if self.index > 0:
                        self.index -= 1
                elif next2 == 67:  # right arrow
                    if self.index < len(self.line):
                        self.index += 1
                elif next2 == 66:  # down arrow
                    if self.history_offset > -1:
                        self.history_offset -= 1
                        self.line = self.get_history(self.history_offset)
                        self.index = len(self.line)
                elif next2 == 65 and self.history_offset < len(self.history) - 1:  # up arrow
                    self.history_offset += 1
                    self.line = self.get_history(self.history_offset)
                    self.index = len(self.line)

        else:
            sys.stdout.write(f'Unknown character: {ch}\n')
            return False

        # Move all the way left, clear the line, write out the prompt,
        # write out the line, move all the way to the left again,
        # and move the cursor to the index.
        # One big write prevents terminal flicker
        sys.stdout.write(
            f"\x1b[1000D\x1b[0K{self.prompt}{self.line}\
            \x1b[1000D\x1b[{len(self.prompt) + self.index}C"
        )

        return False
