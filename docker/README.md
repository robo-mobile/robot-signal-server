# RUN APP IN DOCKER

```shell
# build project
docker-compose  build
# start app with docker-compose 
docker-compose  up
```


```shell
docker build . -t robot
docker run --network host robot
```