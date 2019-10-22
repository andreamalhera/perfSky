# LMU Master's Thesis: Process Mining 2019-2020

## Requirements
- Python 3
- Docker and docker-compose
- Filled envvars.sh: copy ennvars_sample.sh to envvars.sh and fill the blanks.

## Useful development commands ( stored in makefile ):
```
make build  # build docker base image
make test  # run tests in docker container
make external_test # runs tests and start small server to see output images
```

### To see the images generated on a remote machine: 
- On remote machine: `make external test`
- On the local machine:
	```
	lsof -ti:8888 | xargs kill -9
	ssh -N -f -L 8888:localhost:8000 <user@remote_machine.com>
	open "http://localhost:8888/"
	```


## Usefil docker commands: 
- `docker cp /path/to/file container_name:/path/to/file`: To copy files from host into docker container
- `docker ps -a`: List containers
- `docker rm $(docker ps -a | grep 'certain_phrase' | awk '{print $1;}')`: Remove containers that match a certain phrase

## Important documentation: 

- http://pm4py.org/
- https://www.scalyr.com/blog/create-docker-image/
- http://www.processmining.org/event_logs_and_models_used_in_book
