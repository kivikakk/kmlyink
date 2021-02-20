import network
import time
import json

from writer import Writer
import inkplate
import inputsanscompressedregular

import secrets


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(secrets.wifi_ssid, secrets.wifi_key)
        while not sta_if.isconnected():
            pass
    print("network config:", sta_if.ifconfig())


def http_get_json(url):
    import socket

    res = b""
    _, _, host, path = url.split("/", 3)
    addr = socket.getaddrinfo(host, secrets.proxy_port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes("GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host), "utf8"))
    while True:
        packet = s.recv(100)
        if packet:
            res += packet
        else:
            break
    s.close()

    res = str(res, "utf8")
    return json.loads(res[res.index("\r\n\r\n") + 4:])


emails = [
    {"subject": "hello!", "from": "Me <me@me.com>", "date": "2021-01-01 00:00:00 +11"},
    {"subject": "hi!", "from": "Them <them@them.com>", "date": "2020-12-12 00:00:00 +11"},
]
old_emails = emails

# Initialise our Inkplate object
display = inkplate.Inkplate(inkplate.Inkplate.INKPLATE_1BIT)
display.begin()

writer = Writer(display.ipm, inputsanscompressedregular)
writer.set_clip(True, True, False)

OUTER_PADDING = 8
INNER_PADDING = 4
BETWEEN_Y = 5
FONT_HEIGHT = 24

RECT_HEIGHT = FONT_HEIGHT * 3 + INNER_PADDING * 2
TOTAL_HEIGHT = RECT_HEIGHT + BETWEEN_Y

while True:
    do_connect()
    emails = http_get_json("http://" + secrets.proxy_ip + "/mail/" + secrets.secret_key)
    if emails != old_emails:
        old_emails = emails
        try:
            for i, email in enumerate(emails):
                top = OUTER_PADDING + i * TOTAL_HEIGHT
                if top >= 600:
                    break

                is_new = "Seen" not in email["flags"]
                if is_new:
                    display.fillRect(OUTER_PADDING, OUTER_PADDING + i * TOTAL_HEIGHT, inkplate.D_COLS - OUTER_PADDING * 2, RECT_HEIGHT, display.BLACK)
                else:
                    display.drawRect(OUTER_PADDING, OUTER_PADDING + i * TOTAL_HEIGHT, inkplate.D_COLS - OUTER_PADDING * 2, RECT_HEIGHT, display.BLACK)
                from_name, from_email = email["from"].rsplit("<", 1)
                from_email = from_email[:-1]
                if from_name:
                    Writer.set_textpos(display.ipm, OUTER_PADDING + i * TOTAL_HEIGHT + INNER_PADDING, OUTER_PADDING + INNER_PADDING)
                    writer.printstring(from_name, invert=is_new)
                Writer.set_textpos(display.ipm, OUTER_PADDING + i * TOTAL_HEIGHT + INNER_PADDING, inkplate.D_COLS - OUTER_PADDING - INNER_PADDING - writer.stringlen(from_email))
                writer.printstring(from_email, invert=is_new)

                if "Flagged" in email["flags"]:
                    Writer.set_textpos(display.ipm, OUTER_PADDING + i * TOTAL_HEIGHT + INNER_PADDING + FONT_HEIGHT, OUTER_PADDING + INNER_PADDING)
                    writer.printstring("!!", invert=not is_new)

                date = email["date"][:-6]
                Writer.set_textpos(display.ipm, OUTER_PADDING + i * TOTAL_HEIGHT + INNER_PADDING + FONT_HEIGHT, inkplate.D_COLS - OUTER_PADDING - INNER_PADDING - writer.stringlen(date))
                writer.printstring(date, invert=is_new)

                Writer.set_textpos(display.ipm, OUTER_PADDING + i * TOTAL_HEIGHT + INNER_PADDING + FONT_HEIGHT + FONT_HEIGHT, OUTER_PADDING + INNER_PADDING)
                writer.printstring(email["subject"], invert=is_new)
        except ValueError:
            pass

        display.display()

    time.sleep(300)

