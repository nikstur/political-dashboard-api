# REST-API for `political-dashboard.com`

![build badge](https://github.com/nikstur/political-dashboard-api/workflows/build/badge.svg)

## Quick Start

Install Prerequisites.

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Clone the repository.

Inside the directory, start all services.

```bash
docker-compose up --build
```

Navigate to `localhost:8000` to see the generated swagger documentation of the API.

## Development

All commits should be made to the `dev` branch. Afterwards a pull request to the master branch needs to be opened.

To develop locally, two development tools need to be installed:

- [pre-commit](https://pre-commit.com/#installation)
- [poetry](https://python-poetry.org/docs/#installation)

After installing both tools, install the pre-commit hook into the cloned repository from its root directory.

```bash
pre-commit install
```

`pre-commit` is used to ensure code-quality and to make sure that commits will not fail in `GitHub Actions`. After every commit the tools defined in `.pre-commit-config.yaml` will run over every file (modifying files in-place when necessary) and if any of them fail, the commit will be reversed. After making all tools pass, a commit can be successfully made.

Install the dependencies of the `receiver` and `api` service from their respective directories.

```bash
poetry install --no-root
```

Poetry will automatically install dependencies into a virtual environment.

To integrate with a running MongoDB instance, a Docker container can be easily spun up.

```bash
docker run --rm -d --name mongo-dev mongo:4.2.6
```

Then find its IP address.

```bash
docker inspect mongo-dev | grep IPAddress
```
