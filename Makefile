NAME = tv.kvikshaug.no
IMAGE = kvikshaug/${NAME}
IMAGE_GCR = eu.gcr.io/monkey-island-1227/${NAME}

build:
	# Ensure css is compiled before creating the image
	docker-compose run --rm builder sass --scss --update scss:css
	docker-compose build app
	docker tag ${IMAGE} ${IMAGE_GCR}

push:
	gcloud docker push ${IMAGE_GCR}

deploy:
	kubectl delete -f rc.yml -f cron/rc.yml
	kubectl create -f rc.yml -f cron/rc.yml

clean:
	docker rmi ${IMAGE} ${IMAGE_GCR}

.PHONY: build push deploy clean
