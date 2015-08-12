import os
import time
import uuid
import re

import falcon


ALLOWED_IMAGE_TYPES = (
    'image/gif',
    'image/jpeg',
    'image/png',
)


VALID_IMAGE_NAME = re.compile(r'[a-f0-9]{32}\.(jpeg|gif|png)$')


def validate_image_type(req, resp, params):
    if req.content_type not in ALLOWED_IMAGE_TYPES:
        msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
        raise falcon.HTTPBadRequest('Bad request', msg)


def _media_type_to_ext(media_type):
    # Strip off the 'image/' prefix
    return media_type[6:]


def _ext_to_media_type(ext):
    return 'image/' + ext


def _generate_id():
    return uuid.uuid1().hex


class Collection(object):

    def __init__(self, storage_path):
        self.storage_path = storage_path

    @falcon.before(validate_image_type)
    def on_post(self, req, resp):
        image_id = _generate_id()
        ext = _media_type_to_ext(req.content_type)
        filename = image_id + '.' + ext

        image_path = os.path.join(self.storage_path, filename)

        with open(image_path, 'wb') as image_file:
            while True:
                chunk = req.stream.read(4096)
                if not chunk:
                    break

                image_file.write(chunk)

        resp.status = falcon.HTTP_201
        resp.location = '/images/' + filename


class Item(object):

    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_get(self, req, resp, name):
        if not VALID_IMAGE_NAME.match(name):
            raise falcon.HTTPNotFound()

        ext = os.path.splitext(name)[1][1:]
        resp.content_type = _ext_to_media_type(ext)

        image_path = os.path.join(self.storage_path, name)
        try:
            resp.stream = open(image_path, 'rb')
        except IOError:
            raise falcon.HTTPNotFound()
        resp.stream_len = os.path.getsize(image_path)
