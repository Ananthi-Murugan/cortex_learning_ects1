SHELL := /bin/bash
IMAGE_NAME=lrl_cortex_tool_template

venv:
	python3 -m venv .venv &&\
	source .venv/bin/activate &&\
	pip install -r requirements.txt

proto:
	python3 -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./protos/tool.proto

build:
	docker build -t $(IMAGE_NAME) .
start:
	docker run -d --name $(IMAGE_NAME) -p 5000:5000 -it $(IMAGE_NAME):latest

up:
	docker-compose up
dev:
	$(MAKE) build
	$(MAKE) up
	
aws_setup:
	cd $(HOME) &&\
	curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" &&\
	unzip awscliv2.zip &&\
	sudo ./aws/install &&\
	rm awscliv2.zip
	mkdir -p $(HOME)/.aws
	aws configure set default.region us-east-2

aws_login:
	AWS_CONFIG_FILE=../.aws/config AWS_PROFILE=light-d-sso aws sso login --sso-session lilly --no-browser

cats_dev_ecr_login:
	AWS_CONFIG_FILE=../.aws/config AWS_PROFILE=light-d-sso aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 408787358807.dkr.ecr.us-east-2.amazonaws.com

ECR_REPOSITORY=408787358807.dkr.ecr.us-east-2.amazonaws.com/$(IMAGE_NAME)
CURRENT_TAG=dev-sha-$(shell git rev-parse HEAD)

cats_dev_ecr_tag:
	docker tag $(IMAGE_NAME) $(ECR_REPOSITORY):$(CURRENT_TAG)
	
cats_dev_ecr_push: cats_dev_ecr_tag
	docker push $(ECR_REPOSITORY):$(CURRENT_TAG)

cats_dev_ecr_build_and_push: build
	$(MAKE) cats_dev_ecr_push
