-include envvars.mk

envvars.mk: envvars.sh
	sed 's/"//g ; s/=/:=/' < $< > $@

install:
	pip install -r requirements.txt
	pip install .

lint: install
	flake8 perfSky tests

test: install
	python setup.py develop && pytest --durations=100 -vv tests/unit/* tests/integration/*

run: install
	python setup.py develop && python perfSky/run.py

external: run
	cd $(DATA_PATH); \
	python -m http.server 8000


jupyter:
	cd $(NOTEBOOKS_PATH) &&\
	lsof -ti:9000 | xargs kill -9 &&\
	jupyter notebook  --port=9000 --no-browser &
