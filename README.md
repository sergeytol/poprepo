# Poprepo

GitHub repositories popularity checker.

## Description

The service checks whether the provided GitHub repository is popular
or not. Here, popular GitHub repository means one for which `score >= 500` where
`score = num_stars * 1 + num_forks * 2`.

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker-Compose](https://docs.docker.com/compose/install/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- Python >= 3.9

### Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) framework
- [Redis](https://redis.io/)

Python packages:

        "fastapi>=0.68.0,<0.69.0",
        "pydantic>=1.8.0,<2.0.0",
        "uvicorn>=0.15.0,<0.16.0",
        "python-dotenv>=0.20.0,<0.21.0",
        "PyGithub==1.55",
        "django-environ>=0.8.1,<0.9",
        "aioredis==2.0.1",
        "pytest==7.1.1",
        
## Setup

All the commands are should be run in the project root directory

    make install
    
Run it once to prepare the app to work
    
### Start

    make start
    
It will run the app at `0.0.0.0:8000`
The `redis-commander` will be available at `0.0.0.0:8000`
The API spec description will be available at `0.0.0.0:8000/docs`

### Stop

    make stop
    
### Run tests

    make testing
    
## API requests examples

- The API requires `GitHub-Access-Token` header for private repos
- The API supports caching, it can be enabled by adding `X-Use-Caching:On` header to request

### Ping

    curl --location --request GET 'http://0.0.0.0:8000/v1/ping'

### Check repo's popularity

    curl --location --request GET 'http://0.0.0.0:8000/v1/repo/sergeytol/sm/popularity' \
    --header 'GitHub-Access-Token: test123' \
    --header 'x-use-caching: on'

## Docs
The `docs` directory contains `Swagger API docs` and `Postman` collection