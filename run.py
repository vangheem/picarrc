import tornado
import tornado.template
import tornado.websocket
import tornado.web
import tornado.ioloop
import os
import json
from RPi import GPIO


# setup rpi
GPIO.setmode(GPIO.BOARD)

class channels(object):
    forward = 21
    reverse = 19
    left = 11
    right = 13


GPIO.setup(channels.forward, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(channels.reverse, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(channels.left, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(channels.right, GPIO.OUT, initial=GPIO.LOW)

_dir = os.path.dirname(os.path.realpath(__file__))
template_path = os.path.join(_dir, 'templates')

loader = tornado.template.Loader(template_path)


def _action(channel, stop, **kwargs):
    volt = GPIO.HIGH
    if stop:
        volt = GPIO.LOW
    GPIO.output(channel, volt)


class WebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        print 'socket opened'

    def on_message(self, message):
        data = json.loads(message)
        if data['dir'] == 'forward':
            _action(channels.reverse, True)
            _action(channels.forward, **data)
        elif data['dir'] == 'reverse':
            _action(channels.forward, True)
            _action(channels.reverse, **data)
        elif data['dir'] == 'left':
            _action(channels.right, True)
            _action(channels.left, **data)
        elif data['dir'] == 'right':
            _action(channels.left, True)
            _action(channels.right, **data)

    def on_close(self):
        print 'closed'


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(loader.load('index.pt').generate())


static_path = os.path.join(_dir, 'static')

application = tornado.web.Application([
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
    (r'/socket', WebSocket),
    (r'/', IndexHandler)
])


if __name__ == "__main__":
    application.listen(8000, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()
