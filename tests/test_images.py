import json
import re
import uuid
import os

from falcon.testing import TestBase
import falcon

from app import (
    api,
    STORAGE_PATH,
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

FIXTURES_DIR = os.path.join(CURRENT_DIR, 'fixtures')

VALID_IMAGE_NAME = re.compile(r'[a-f0-9]{32}\.(jpeg|gif|png)$')


def read_file(filepath):
    with open(filepath, 'rb') as content_file:
        return content_file.read()


class TestImage(TestBase):

    def tearDown(self):
        filelist = [f for f in os.listdir(STORAGE_PATH) if VALID_IMAGE_NAME.match(f)]
        for f in filelist:
            os.remove(os.path.join(STORAGE_PATH, f))
        super().tearDown()

    def before(self):
        self.api = api

    def image_type(self, image_type):
        filepath = os.path.join(FIXTURES_DIR, 'image.{}'.format(image_type))
        image_content = read_file(filepath)
        body = self.simulate_request(
            '/images',
            method='POST',
            body=image_content,
            decode='utf-8',
            headers={'content-type': 'image/{}'.format(image_type)})
        self.assertEqual(body, '')
        response = self.srmock
        self.assertEqual(response.status, falcon.HTTP_201)
        location = response.headers_dict['location']
        self.assertTrue(location.startswith('/images/'))
        image_file = location.split('/images/')[1]
        self.assertTrue(VALID_IMAGE_NAME.match(image_file))
        self.assertTrue(location.endswith('.{}'.format(image_type)))
        self.assertEqual(response.headers_dict['content-length'], '0')
        filepath = os.path.join(STORAGE_PATH, image_file)
        image_content2 = read_file(filepath)
        self.assertEqual(image_content, image_content2)

    def test_upload_jpeg(self):
        self.image_type('jpeg')

    def test_upload_gif(self):
        self.image_type('gif')

    def test_upload_png(self):
        self.image_type('png')

    def test_upload_not_allowed_method(self):
        body = self.simulate_request(
            '/images',
            method='GET',
            body='images',
            decode='utf-8',
            headers={'content-type': 'image/jpeg'})
        self.assertEqual(body, '')
        response = self.srmock
        self.assertEqual(response.status, falcon.HTTP_405)
        self.assertEqual(response.headers_dict['allow'], "POST, OPTIONS")
        self.assertEqual(response.headers_dict['content-length'], '0')

    def test_upload_not_allowed_image_type(self):
        body = self.simulate_request(
            '/images',
            method='POST',
            body='images',
            decode='utf-8',
            headers={'content-type': 'image/jpeg2'})
        msg = {
            'title': 'Bad request',
            'description': 'Image type not allowed. Must be PNG, JPEG, or GIF'
        }
        self.assertEqual(json.loads(body), msg)
        response = self.srmock
        self.assertEqual(response.status, falcon.HTTP_400)
        self.assertEqual(
            response.headers_dict['content-type'],
            'application/json'
        )

    def test_upload_options_method(self):
        body = self.simulate_request(
            '/images'.format(image=uuid.uuid1().hex),
            method='OPTIONS',
            body='images',
            decode='utf-8',
            headers={'content-type': 'image/jpeg'})
        self.assertEqual(body, '')
        response = self.srmock
        self.assertEqual(response.status, falcon.HTTP_204)
        self.assertEqual(response.headers_dict['allow'], "POST")

    def test_get_image_invalid_name(self):
        body = self.simulate_request(
            '/images/image.jpeg',
            method='GET',
            body='images',
            decode='utf-8')

        response = self.srmock
        self.assertEqual(response.status, falcon.HTTP_404)
        self.assertEqual(response.headers_dict['content-length'], '0')

    def test_get_image_not_found(self):
        body = self.simulate_request(
            '/images/{image}.jpeg'.format(image=uuid.uuid1().hex),
            method='GET',
            body='images',
            decode='utf-8')

        response = self.srmock
        self.assertEqual(response.status, falcon.HTTP_404)
        self.assertEqual(response.headers_dict['content-length'], '0')

    def test_get_image_not_allowed_method(self):
        body = self.simulate_request(
            '/images/{image}.jpeg'.format(image=uuid.uuid1().hex),
            method='POST',
            body='images',
            decode='utf-8',
            headers={'content-type': 'image/jpeg'})
        self.assertEqual(body, '')
        response = self.srmock
        self.assertEqual(response.status, falcon.HTTP_405)
        self.assertEqual(response.headers_dict['allow'], "GET, OPTIONS")
        self.assertEqual(response.headers_dict['content-length'], '0')

    def test_get_image_options_method(self):
        body = self.simulate_request(
            '/images/{image}.jpeg'.format(image=uuid.uuid1().hex),
            method='OPTIONS',
            body='images',
            decode='utf-8',
            headers={'content-type': 'image/jpeg'})
        self.assertEqual(body, '')
        response = self.srmock
        self.assertEqual(response.status, falcon.HTTP_204)
        self.assertEqual(response.headers_dict['allow'], "GET")
