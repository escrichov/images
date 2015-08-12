import os
from wsgiref import simple_server

import falcon

import images


api = application = falcon.API()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

STORAGE_PATH = os.path.join(CURRENT_DIR, 'uploads')

image_collection = images.Collection(STORAGE_PATH)
image = images.Item(STORAGE_PATH)

api.add_route('/images', image_collection)
api.add_route('/images/{name}', image)


# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
