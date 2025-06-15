#
# Convenience Makefile
# Useful reference: https://makefiletutorial.com

GIT_SHA := $(shell git rev-parse --short HEAD)
VERSION ?= 0.0.0-dev0.${GIT_SHA}
PYTHON_VERSION := $(shell echo "${VERSION}" | sed -e 's/-dev0\./-dev0+/')
WHEEL_VERSION := $(shell echo "${VERSION}" | sed -e 's/-dev0\./.dev0+/')

ROOT_PATH := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

PYTHON_SOURCES := $(shell find src/mrmat_python_api_fastapi -name '*.py')
PYTHON_TARGET := dist/mrmat_python_api_fastapi-${WHEEL_VERSION}-py3-none-any.whl
CONTAINER_SOURCES := $(shell find var/container)
HELM_SOURCES := $(shell find var/helm)
HELM_TARGET := dist/mrmat-python-api-fastapi-$(VERSION).tgz

# My cluster names default to the hostname they run on
CLUSTER_NAME := $(shell hostname -s)
# Can be either 'istio-sidecar' or 'istio-ambient'
MESH := istio-ambient
# Can be 'ingress', 'gateway-api' or 'istio'
EDGE := gateway-api

# How the container then connects to its datastore
API_DB_URL="sqlite:////data/db.sqlite3"

# All of this can be overridden by the include in ~/etc/api-secrets.mk
-include ~/etc/secrets.mk

all: python container helm
python: $(PYTHON_TARGET)
helm: $(HELM_TARGET)

$(PYTHON_TARGET): $(PYTHON_SOURCES)
	MRMAT_VERSION="${PYTHON_VERSION}" python -mbuild -n --wheel

$(HELM_TARGET): $(HELM_SOURCES) container
	helm package \
		--version $(VERSION) \
		--app-version "$(VERSION)" \
		--destination dist/ \
		var/helm
	helm push dist/mrmat-python-api-fastapi-$(VERSION).tgz oci://localhost:5001/charts

container: $(CONTAINER_SOURCES) $(PYTHON_TARGET)
	docker build \
		-f var/container/Dockerfile \
		-t localhost:5001/mrmat-python-api-fastapi:$(VERSION) \
		--build-arg GIT_SHA=$(GIT_SHA) \
		--build-arg MRMAT_VERSION=$(VERSION) \
		--build-arg WHEEL=$(PYTHON_TARGET) \
		$(ROOT_PATH)
	docker push localhost:5001/mrmat-python-api-fastapi:$(VERSION)

helm-install: $(HELM_TARGET)
	kubectl create ns mpafastapi || true
	if test "$(MESH)" == "istio-sidecar"; then kubectl label --overwrite ns mpafastapi istio-injection=true; fi
	if test "$(MESH)" == "istio-ambient"; then kubectl label --overwrite ns mpafastapi istio.io/dataplane-mode=ambient; fi
	helm upgrade \
		mrmat-python-api-fastapi \
		${HELM_TARGET} \
		--install \
		--wait \
		--force \
		--namespace mpafastapi \
		--set cluster.name=$(CLUSTER_NAME) \
		--set cluster.mesh=$(MESH) \
		--set edge.kind=$(EDGE) \
		--set config.db_url=$(API_DB_URL)

helm-uninstall:
	helm delete -n mpafastapi mrmat-python-api-fastapi

clean:
	rm -rf build dist
