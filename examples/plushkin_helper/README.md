# Docker

Create docker images and execute the container.

```sh
cd examples/plushkin_helper

# Build docker image
docker build -t plushkin .

# Find duplicates
docker run --rm -v <path>:/volume -it plushkin /volume

# Find duplicates for deletion 
docker run --rm -v <path>:/volume -it plushkin -d /volume
```
