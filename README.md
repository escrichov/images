# Manage Images

Upload images to the server and download them.

## Develop

### Create virtualenv
```bash
virtualenv env
```

### Install requirements
```bash
env/bin/pip install -r requirements.txt
```

### Run tests
```bash
env/bin/nosetests
```

### Run test server
```bash
env/bin/python app.py
```

### Run production server
```bash
env/bin/uwsgi --http :8000 --wsgi-file app.py
```

### Install httpie
```bash
brew install httpie
```

### Upload images
```bash
http POST localhost:8000/images Content-Type:image/jpeg < tests/fixtures/image.jpeg 
http POST localhost:8000/images Content-Type:image/png < tests/fixtures/image.png
http POST localhost:8000/images Content-Type:image/gif < tests/fixtures/image.gif
```

### Get images
```bash
curl localhost:8000/images/20cb8df6412111e5a0f80242ac11000c.jpeg > image.jpeg
```

## Deploy

[Docker deployment](https://github.com/escrichov/images/blob/master/docker/README.md)
