-include envvars.mk

envvars.mk: envvars.sh
	sed 's/"//g ; s/=/:=/' < $< > $@

install:
	docker login -u $(DOCKER_USERNAME) -p $(DOCKER_PASSWORD)
	docker build -t processmining_image -f Dockerfile .

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
