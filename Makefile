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

# Can be either 'sidecar' or 'ambient'
ISTIO := ambient

all: python container helm
python: $(PYTHON_TARGET)
helm: $(HELM_TARGET)

$(PYTHON_TARGET): $(PYTHON_SOURCES)
	MRMAT_VERSION="${PYTHON_VERSION}" python -mbuild -n --wheel

$(HELM_TARGET): $(HELM_SOURCES) container
	helm package \
		--app-version "$(VERSION)" \
		--version $(VERSION) \
		--destination dist/ \
		var/helm

container: $(PYTHON_TARGET) $(CONTAINER_SOURCES)
	docker build \
		-f var/container/Dockerfile \
		-t localhost:5001/mrmat-python-api-fastapi:$(VERSION) \
		--build-arg MRMAT_VERSION=$(VERSION) \
		--build-arg WHEEL=$(PYTHON_TARGET) \
		$(ROOT_PATH)
	docker push localhost:5001/mrmat-python-api-fastapi:$(VERSION)

helm-install: $(HELM_TARGET)
	kubectl create ns mpafastapi || true
	if test "$(ISTIO)" == "sidecar"; then kubectl label --overwrite ns mpafastapi istio-injection=true; fi
	if test "$(ISTIO)" == "ambient"; then kubectl label --overwrite ns mpafastapi istio.io/dataplane-mode=ambient; fi
	helm upgrade \
		mrmat-python-api-fastapi \
		${HELM_TARGET} \
		--install \
		--wait \
		--force \
		--namespace mpafastapi \
		--set istio=$(ISTIO)

helm-uninstall:
	helm delete -n mpafastapi mrmat-python-api-fastapi

clean:
	rm -rf build dist
