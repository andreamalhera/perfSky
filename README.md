# The Performance Skyline
Performance mining from event logs is a central element to manage and improve business processes.
Established performance analysis techniques are either based on control-flow models, which simulate
all possible execution paths for a process at once, or methods that propose extracting performance
features from only one timestamp. This thesis integrates interval-based methods from sequence pattern
mining into process mining to discover performance process models from event logs that include both,
start and end event timestamps. In addition it introduces the _performance skyline_, which
describes the series of events that lead to the worst case duration of a process and  enables novel
extensions for further process discovery, conformance checking and process enhancement. Executed
experiments on real event logs show that presented models assist detecting and classifying trace
anomalies into multiple categories.

If you'd like to learn more about how it works, see References below.

Brought to you by [Andrea Maldonado](andreamalher.works@gmail.com)

## Presentation slides, paper and master thesis:
* [Performance Skyline Presentation](master_thesis/slides_inferring_process_performance_models_from_interval_events_using_the_performance_skyline.pdf)
* [Performance Skyline: Inferring Process Performance Models from Interval Events Paper](https://www.springerprofessional.de/en/performance-skyline-inferring-process-performance-models-from-in/19021296)
* [Performance Skyline Master's Thesis](master_thesis/written_composition_inferring_process_performance_models_from_interval_events_using_the_performance_skyline.pdf)

## Structure
This directory contains:
- [Makefile](): Defines commands to run with this pipeline
- [envvars_sample.sh](): Sample to fill in environmental variables to run this pipeline
- [requirements.txt](): Specifies necessary requirements to run in conda environment
- [setup.py](): Specifies package out of this project

Directories are divided into [master thesis content](master_thesis/), [jupyter notebooks](notebooks/), [tests](tests/), [data used for experiments](data/) and runable [code](perfSky/).
The following notebook can be found:
- [tuto.ipynb](notebooks/tuto.ipynb): Presents an example for visualization.

The code is divided in three main modules, [preprocessing](perfSky/preprocessing), [skyline](perfSky/skyline.py) and [Visualizer](perfSky/Visualizer.py). The first contains methods to convert '.log' files into '.csv' containing interval events, as explained in the [master's thesis](master_thesis/Performance_Skyline_Andrea_Maldonado.pdf).
The plots module contains visualization methods to project traces from an interval events '.csv' into the process geometric representation. Skyline contains methods to compute the performance skyline and the average trace from a trace set.


## Installation
### Requirements:
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Python 3.9+
- Filled envvars.sh: copy ennvars_sample.sh to envvars.sh and fill the blanks.

### For experimenting on jupyter notebooks:
```
conda create -n py39 python=3.9
conda activate py39

#install requirements
pip install .
jupyter lab --port=9000 # To tunnel to local machine add: --no-browser &

# In local machine (only in case you are tunneling): 
ssh -N -f -L 8888:localhost:9003 <user@remote_machine.com>
```

### Useful development commands ( stored in makefile ):
```
make install  # install as pip package in conda enviroment
make test  # run tests with pytest
make run # run the pipeline
make external # run the pipeline and start small server to see output images
```

## Usage from '.log's to performance skyline exploration plots 
To run this pipeline in other luigi logs follow these steps: 
- To preprocess logs, specify the `PROCESS_NAME`, `LUIGI_LOG_PATH` and `OUTPUT_PATH` in [run.py](perfSky/run.py)
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

## References
The algorithm used by `perfSky` is taken directly from the original paper by Maldonado, Sontheim, Richter and Seidl. If you would like to discuss the paper, or corresponding research questions on temporal process mining (we have implemented a few other algorithms as well) please email the authors.
