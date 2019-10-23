-include envvars.mk

envvars.mk: envvars.sh
	sed 's/"//g ; s/=/:=/' < $< > $@

install:
	docker login -u $(DOCKER_USERNAME) -p $(DOCKER_PASSWORD)
	docker build -t processmining_image -f Dockerfile .

lint: install
	docker-compose run --rm -w /code processmining bash -c "flake8 processmining tests"

test: install
	docker-compose run --rm -w /code processmining bash -c "./gepetto.sh 'pytest -vv tests/*'"

run: install
	docker-compose run --rm -w /code processmining bash -c "./gepetto.sh 'python processmining/run.py'"

external: run
	cd $(DATA_PATH); \
	python -m SimpleHTTPServer 8000
