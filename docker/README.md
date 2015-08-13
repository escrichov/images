# Create machine

```bash
export DIGITAL_OCEAN_TOKEN=token

docker-machine create \
--driver digitalocean \
--digitalocean-access-token=$DIGITAL_OCEAN_TOKEN \
--digitalocean-region "fra1" \     
machine
```

# Set docket environment
```bash
eval "$(docker-machine env machine)"
````

# Run Containters

## Method 1 - Docker compose

```bash
docker-compose up -d
````

## Method 2 - Manually

### App Server

#### Create image

```bash
docker build -t docker_app_server ./docker-images
````

#### Run container

```bash
docker run -d -p 8000:8000 --name app_server docker_app_server
````

###  Nginx

#### Create image

```bash
docker build -t docker_nginx ./docker-nginx
````

#### Run container

```bash
docker run \
-d \
--name nginx \
--link app_server:app_server \
-p 80:80 -p 443:443 \
docker_nginx
````
