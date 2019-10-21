-include envvars.mk

envvars.mk: envvars.sh
	sed 's/"//g ; s/=/:=/' < $< > $@

install:
	echo $(DOCKER_USERNAME)
	docker login -u $(DOCKER_USERNAME) -p $(DOCKER_PASSWORD)
	docker build -t processmining_image .