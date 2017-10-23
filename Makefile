SHELL := /bin/bash

default: up

up:
	docker-compose -f docker-compose.yml up -d

demo1:
	docker-compose -f docker-compose.yml run --rm client python main.py -l True 

demo2:
	docker-compose -f docker-compose.yml run --rm client python main.py -l True -i 0.05

log:
	docker-compose -f docker-compose.yml logs -f

clean:
	docker-compose -f docker-compose.yml stop && docker-compose -f docker-compose.yml rm -f

build:
	docker-compose -f docker-compose.build.yml build

deploy:
	docker deploy -c docker-compose.yml iot_enviro
