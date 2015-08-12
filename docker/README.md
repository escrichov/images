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

# Create image

```bash
docker build -t image .
````

# Run container

```bash
docker run -d -p 80:80 --name img image 
````
