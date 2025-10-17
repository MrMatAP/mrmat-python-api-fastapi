# MrMat :: Python :: API :: FastAPI

[![CI](https://github.com/MrMatOrg/mrmat-python-api-fastapi/actions/workflows/ci.yml/badge.svg)](https://github.com/MrMatOrg/mrmat-python-api-fastapi/actions/workflows/ci.yml)

Boilerplate (and playground) for a code-first Python FastAPI API.

## How to build this

### Interactively

The project uses the [uv build tool](https://docs.astral.sh/uv/). Install it first, then simply run `uv build --wheel`.

All interactive builds default their version to '0.0.0.dev0', which we use as a marker that this is a locally produced
build which should not go into production. You can override this behaviour by setting the 'MRMAT_VERSION' environment
variable to the desired version, but doing so is discouraged.

### Continuous Integration

GitHub Actions will trigger builds for pushes and pull requests. A merge push onto the main branch will additionally
create a release.

All builds on branches other than main will have their version calculated from the MAJOR, MINOR and GITHUB_RUN_NUMBER
environment variables with a '.dev0' suffix appended. You can set the MAJOR and MINOR variables in
`.github/workflows/build.yml`. Builds resulting from a merge push onto the main branch will not have a suffix.

The resulting code is aware of its version at build-time via the extra `src/ci` module, which is explicitly excluded from
the distribution. Pythons own `importlib.metadata` is then used to make the version available at runtime.

### Container Image

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
