# MrMat :: Python :: API :: FastAPI

[![Build](https://github.com/MrMatOrg/mrmat-python-api-fastapi/actions/workflows/build.yml/badge.svg)](https://github.com/MrMatOrg/mrmat-python-api-fastapi/actions/workflows/build.yml)

Boilerplate (and playground) for a code-first Python FastAPI API.

## How to build this

Create a virtual environment, then:

```shell
(venv) $ pip install -r requirements.txt
(venv) $ python -m build -n --wheel
```

If you intend to run the testsuite or work on the code, then also install the requirements from `requirements.dev.txt`. You can run the testsuite using

```shell
(venv) $ PYTHONPATH=src pytest tests
```

The resulting wheel is installable and knows its runtime dependencies. Any locally produced wheel will have version 0.0.0.dev0. This is intentional to distinguish local versions from those that are produced as releases in GitHub. You can override this behaviour by setting the `MRMAT_VERSION` environment variable to the desired version.

You can produce a container image and associated Helm chart using the provided Makefile:

```shell
$ make container

# Optionally install the produced container image in the current Kubernetes context
$ make helm-install
```

## How to run this

To run a local development instance straight from the code:

```shell
$ fastapi dev src/mrmat_python_api_fastapi/app.py
```

To run from an installed wheel:

```shell
$ uvicorn --host 0.0.0.0 --port 8000 mrmat_python_api_fastapi.app:app
```

Or you can just start the container image or Helm chart. Both are declared in `var/container` and `var/helm` respectively and used by the top-level Makefile.

## How to configure this

When you do not explicitly configure anything the app will use an ephemeral in-memory SQLite database. You can change this to PostgreSQL by:

* overriding the `config.db_url` variable of the Helm chart, or
* setting the `APP_CONFIG_DB_URL` environment variable, or
* creating a config file in JSON setting `db_url`

The app will pick up the config file from the path set in the `APP_CONFIG` environment variable, if it is set. Note that the `APP_CONFIG_DB_URL` environment variable overrides the setting in the configuration file.
