# LMU Master's Thesis: Process Mining 2019-2020
## Process Discovery

### Important documentation: 

- http://pm4py.org/
- https://www.scalyr.com/blog/create-docker-image/
- http://www.processmining.org/event_logs_and_models_used_in_book

## Installation 

```
docker pull javert899/pm4py:latest
docker run -it javert899/pm4py:latest bash

```
In the docker container run: 
```
pip install pm4py
python -c "import pm4py"

apt-get install xdg-utils
```
To copy files from host into docker container: 
```
docker cp /path/to/file container_name:/path/to/file
```
Find the container's name with 
```
docker ps
```