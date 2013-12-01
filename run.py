import tornado
import tornado.template
import tornado.websocket
import tornado.web
import tornado.ioloop
import os
import json

_dir = os.path.dirname(os.path.realpath(__file__))
template_path = os.path.join(_dir, 'templates')

loader = tornado.template.Loader(template_path)


def forward(stop=False, **kwargs):
    print 'forward'


def reverse(stop=False, **kwargs):
    print 'reverse'


def left(stop=False, **kwargs):
    print 'left'


def right(stop=False, **kwargs):
    print 'right'


class WebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        print 'socket opened'

    def on_message(self, message):
        data = json.loads(message)
        if data['dir'] == 'forward':
            forward(**data)
        elif data['dir'] == 'reverse':
            reverse(**data)
        elif data['dir'] == 'left':
            left(**data)
        elif data['dir'] == 'right':
            right(**data)

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
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
