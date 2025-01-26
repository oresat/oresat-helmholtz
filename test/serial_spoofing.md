# How to test/run the program on a linux machine without the actual cage

We are going to use `pty`'s (pseudo terminals) to act as virtual serial ports.
In order to initialize the serial ports use `socat` like so:
```
[user@mylaptop ~]$ socat -d -d pty,echo=1,cr pty,echo=1,cr
2025/01/26 12:24:22 socat[7152] N PTY is /dev/pts/4
2025/01/26 12:24:22 socat[7152] N PTY is /dev/pts/5
2025/01/26 12:24:22 socat[7152] N starting data transfer loop with FDs [5,5] and [7,7]
```

We can see from the output that `socat` has created two pseudo-terminals which we may use as
virtual serial ports. From the output above we can determine the directory locations of these 
ports. `/dev/pts/4` and `/dev/pts/5`

You can think of these serial ports as two ends of USB cable, one of which we want to attach to
our computer, and the other we wish to attach to the Helmholtz Cage Controller (HCC) program. 
Take a moment to decide which end is which.

For my example case I will attach `/dev/pts/4` to my computer, and attach `/dev/pts/5` to the
HCC. The following two sections will show how these attachments can be made.

## Attaching `/dev/pts/4` to computer terminal
Since the pseudo terminal already exists on my computer, we don't need to 'attach' it anywhere.
We can easily *listen* to it by opening a new terminal window (terminal 2) and running the 
following command,
```
[user@mylaptop ~]$ cat < /dev/pts/4
|
```

This command will wait for messages to appear in the `/dev/pts/4` file location and prints
these messages in the terminal. This will become very useful once we've attached the other end
to the HCC, but for now it's just waiting around.

> For a quick idea of what's going on, open another terminal window (terminal 3) and type
> ```
> [user@mylaptop ~]$ echo 'I <3 PSAS' > /dev/pts/5
> ```
> You will see this message appear in your other terminal window! (terminal 2)

## Attaching `/dev/pts/5` to the HCC
Now, for your convenience the HCC program allows you to specify a debug port over which it will 
route ALL messages (i.e. power supply voltage settigns, h-bridge polarity settings, 
magnetometer queries, etc) through. This is through the `-d` or `--debug-port` options.
You may use it like so,
```
[user@mylaptop ~]$ python main.py -d '/dev/pts/5'
```
This will start up the program and you will have successfully emulated the Helmholtz cage control
environment. This allows you to view the message traffic transmitted by the HCC program to Oresat's
HCC. Try running a command such as `voltage X 10` and see what is communicated on terminal 2.
