pipenv-install:
	@echo "******************************************"
	@echo "*    Installing pipenv requirements      *"
	@echo "******************************************"
	export PIPENV_NO_INHERIT=1 && pipenv install --dev

pipenv-shell:
	@echo "******************************************"
	@echo "*             pipenv shell               *"
	@echo "******************************************"
	pipenv shell

dev-init:
	@echo "******************************************"
	@echo "*       Preparing dev environment        *"
	@echo "******************************************"
	cp docker-compose.yml-dist docker-compose.yml
	cp env/env-dist env/.env.dev

build:
	@echo "******************************************"
	@echo "*           Building services            *"
	@echo "******************************************"
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose stop

down:
	docker-compose down

testing:
	@echo "******************************************"
	@echo "*                 Testing                *"
	@echo "******************************************"
	docker-compose run --rm poprepo-api-test

install: pipenv-install dev-init build
	@echo "All done."
