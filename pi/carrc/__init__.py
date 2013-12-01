import tornado
import os

_dir = os.path.dirname(os.path.realpath(__file__))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        pass


static_path = os.path.join(_dir, 'static')

applicatoin = tornado.web.Applicatoin([
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
    (r'/', IndexHandler)
])


