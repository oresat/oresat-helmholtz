# How to test/run the program on a linux machine without the actual cage

We are going to use pty (pseudo terminals) to act as virtual serial ports.
In order to initialize the serial ports use `socat` like so:
```socat -d -d pty,echo=1,cr pty,echo=1,cr```

This should create two serial ports such as
`/dev/pts/4`
`/dev/pts/5`

Further developments on the way.
