# kmlyink

Just messing around with an [Inkplate](https://inkplate.io).

This repo has two parts:

- a Dockerised IMAP proxy written in Ruby.

  It speaks plain HTTP, like an ESP can manage.  It just fetches your Inbox
  listing and puts it in JSON.

- a MicroPython module that connects to your wifi, speaks to the IMAP proxy,
  and formats it into the display.


## Security

Non-existent.  There is a very light "secret key" used to fetch your mail from
the proxy.  Don't run this outside home, and preferably have a separate guest
network.

## Fonts

I use Peter Hinch's
[micropython-font-to-py](https://github.com/peterhinch/micropython-font-to-py)
to create a version of [Input](https://input.fontbureau.com) suitable for use.
Here's the command line to do that:

```
./font_to_py.py InputSansCompressed-Regular.ttf -x 24 inputsanscompressedregular.py
```

This repository also includes the `Writer` from the same project.  It's MIT
licensed, (c) Peter Hinch.

## License

MIT license.
