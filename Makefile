-include envvars.mk

envvars.mk: envvars.sh
	sed 's/"//g ; s/=/:=/' < $< > $@

install:
	docker login -u $(DOCKER_USERNAME) -p $(DOCKER_PASSWORD)
	docker build -t processmining_image -f Dockerfile .

test: install
	docker-compose run  --rm -w /code processmining bash -c "pytest -vv tests/test.py ;\rm -R tests/__pycache__/"

external_test: test
	cd $(DATA_PATH); \
	python -m SimpleHTTPServer 8000
