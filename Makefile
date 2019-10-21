install:
	source envvars.sh
	docker login -u $(DOCKER_USERNAME) -p $(DOCKER_PASSWORD)
	docker build -t processmining_image .