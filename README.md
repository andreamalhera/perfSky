# LMU Master's Thesis: Inferring Process Performance Models from Interval Events using the Performance Skyline

## Abstract
Performance mining from event logs is a central element to manage and improve business processes.
Established performance analysis techniques are either based on control-flow models, which simulate
all possible execution paths for a process at once, or methods that propose extracting performance
features from only one timestamp. This thesis integrates interval-based methods from sequence pattern
mining into process mining to discover performance process models from event logs that include both,
start and end event timestamps. In addition it introduces the \textit{performance skyline}, which
describes the series of events that lead to the worst case duration of a process and  enables novel
extensions for further process discovery, conformance checking and process enhancement. Executed
experiments on real event logs show that presented models assist detecting and classifying trace
anomalies into multiple categories.

## Presentation Slides
* [Performance Skyline Presentation](master_thesis/Inferring_Process_Performance%20Models%20from_Interval_Events_using_the_Performance_Skyline.pdf)
* [Performance Skyline Master's Thesis](master_thesis/Performance_Skyline_Andrea_Maldonado.pdf)

## Structure
This directory contains:
- [Dockerfile]() and [docker-compose.yml](): Describe set-up for docker container to run this pipeline
- [gepetto.sh](): Installs package inside docker container.
- [Makefile](): Defines commands to run with this pipeline
- [envvars_sample.sh](): Sample to fill in environmental variables to run this pipeline
- [requirements.txt](): Specifies necessary requirements to run in conda environment
- [setup.py](): Specifies package out of this project

Directories are divided into [master thesis content](master_thesis/), [jupyter notebooks](notebooks/), [tests](tests/), [data used for experiments](data/) and runable [code](processmining/).
The following notebooks contain prototypes of parts also implemented in the code: 
- [boxplot.ipynb](notebooks/boxplot.ipynb)
- [logsToCatts.ipynb](notebooks/logsToCatts.ipynb)
- [toyExampleToCatts.ipynb](notebooks/toyExampleToCatts.ipynb)
- [pointTransformer.ipynb](notebooks/pointTransformer.ipynb)
- [performance_skyline_anomalies.ipynb](notebooks/performance_skyline_anomalies.ipynb): Used for experiments with the performance skyline  in new logs, specifically for anomaly detection 

The code is divided in two main modules, [preprocessing](processmining/preprocessing) and [plot](processmining/plot). The first contains methods to convert '.log' files into '.csv' containing interval events, as explained in the [master's thesis](master_thesis/Performance_Skyline_Andrea_Maldonado.pdf).
The plots module contains visualization methods to project traces from an interval events '.csv' into the process geometric representation. It also contains methods to compute the performance skyline and the average trace from a trace set.


## Installation:
### Requirements
- Python 3.6
- Docker and docker-compose
- Filled envvars.sh: copy ennvars_sample.sh to envvars.sh and fill the blanks.

### For experimenting on jupyter notebooks:
```
conda create -n performance-skyline_venv python=3
conda activate performance-skyline_venv

#install requirements
pip install -r requirements.txt
jupyter lab --port=9000 # To tunnel to local machine add: --no-browser &

# In local machine (only in case you are tunneling): 
ssh -N -f -L 8888:localhost:9003 <user@remote_machine.com>
```

### Useful development commands ( stored in makefile ):
```
make install  # build docker base image
make test  # run tests in docker container
make run # run the pipeline in docker container
make external # run the pipeline and start small server to see output images
```

### Usage from '.log's to performance skyline exploration plots: 
To run this pipeline in other luigi logs follow these steps: 
- To preprocess logs, specify the `PROCESS_NAME`, `LUIGI_LOG_PATH` and `OUTPUT_PATH` in [run.py](processmining/run.py)
- `make run` to convert logs into single `.csv` file containing preprocessed trace set with interval events.
- Specify location of trace set `.csv` in [performance_skyline_anomalies](notebooks/performance_skyline_anomalies.ipybn) notebook and run it.
### To see the images generated on a remote machine: 
- On remote machine: `make external test`
- On the local machine:
	```
	lsof -ti:8888 | xargs kill -9
	ssh -N -f -L 8888:localhost:8000 <user@remote_machine.com>
	open "http://localhost:8888/"
	```


## Useful docker commands: 
- `docker cp /path/to/file container_name:/path/to/file`: To copy files from host into docker container
- `docker ps -a`: List containers
- `docker rm $(docker ps -a | grep 'certain_phrase' | awk '{print $1;}')`: Remove containers that match a certain phrase
- `docker run -it -v $PWD:/code -v $DATA_PATH:/code/data container_name:latest bash`: To experiment inside container
	Note: The last will take the container as in Docker-Hub some packages might be missing.
	To update container after intalling additional packages  see 'Update container in Docker Hub'

### Update container in Docker Hub
```
docker pull container_name:latest
docker run -it -v $PWD:/code -v $DATA_PATH:/code/data container_name:latest bash

# Install everything you need here

docker commit container_id container_name # Container_id is whatever comes after 'root@'
docker tag image_id container_id:tag_name
docker push container_id
```


## Important sources: 

- http://pm4py.org/
- https://www.scalyr.com/blog/create-docker-image/
- http://www.processmining.org/event_logs_and_models_used_in_book
