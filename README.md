# REST-API for `political-dashboard.com`

![build badge](https://github.com/nikstur/political-dashboard-api/workflows/build/badge.svg)

## Quick Start

Install the prerequisites:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Clone the repository

Inside the directory, build and start all services

```bash
docker-compose up --build
```

Navigate to `api.political-dashboard.localhost` to see the generated SwaggerUI
documentation of the API.

## Development

The master branch should always contain a working, deployable
version of the services.

To develop locally, two development tools need to be installed:

- [pre-commit](https://pre-commit.com/#installation)
- [poetry](https://python-poetry.org/docs/#installation)

After installing both tools, install the pre-commit hook into the cloned
repository from its root directory.

```bash
pre-commit install
```

`pre-commit` is used to ensure quality and reduce merge conflicts. The
`GitHub Actions` pipeline will run the pre-commit hooks on all files after every
commit.

Install the dependencies of the `ingester` and `api` service from their
respective directories to utilise auto-formatting and linting.

```bash
poetry install --no-root
```

Poetry will install the dependencies into a virtual environment.
