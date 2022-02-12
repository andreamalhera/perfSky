-include envvars.mk

envvars.mk: envvars.sh
	sed 's/"//g ; s/=/:=/' < $< > $@

install:
	docker login -u $(DOCKER_USERNAME) -p $(DOCKER_PASSWORD)
	docker build -t processmining_image -f Dockerfile .

lint: install
	docker-compose run --rm -w /code processmining bash -c "flake8 processmining tests"

test: install
	docker-compose run --rm -w /code processmining bash -c "./gepetto.sh 'pytest --durations=100 -vv tests/unit/* tests/integration/*'"

run: install
	docker-compose run --rm -w /code processmining bash -c "./gepetto.sh 'python processmining/run.py'"

external: run
	cd $(DATA_PATH); \
	python -m http.server 8000

server: install
	docker-compose run --rm -w /code processmining bash -c "./gepetto.sh 'python print('Hello docker')'"
	cd $(DATA_PATH); \
	python -m http.server 8000

jupyter:
	cd $(NOTEBOOKS_PATH) &&\
lsof -ti:9000 | xargs kill -9 &&\
jupyter notebook  --port=9000 --no-browser &
