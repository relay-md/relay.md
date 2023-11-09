ROOT_DIR := $(shell pwd)
PROJECT_NAME := api
RELEASE_VERSION ?= $(shell git describe --always)
RELEASE_DATE := $(shell date -u +'%Y-%m-%dT%H:%M:%SZ')
PACKAGE_DIR=api

IMAGE_REGISTRY := registry.infra.chainsquad.com
IMAGE_NAME := channelmd/$(PROJECT_NAME)
DEPLOY_KEY := $(shell [ -f ~/.ssh/id_rsa ] && cat ~/.ssh/id_rsa | base64 -w0)
DOCKER_BUILD_ARGS := --build-arg BUILD_DATE=$(RELEASE_DATE) \
                     --build-arg VCS_REF=$(RELEASE_VERSION) \
                     --build-arg SSH_KEY=$(DEPLOY_KEY)

.PHONY: clean
clean: clean-build clean-pyc clean-pycache

.PHONY: clean-build
clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf __pycache__/ .eggs/ .cache/
	rm -rf .tox/ .pytest_cache/ .benchmarks/ .mypy_cache htmlcov

.PHONY: clean-pycache
clean-pycache:
	find . -name __pycache__ -exec rm -rf {} +

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

.PHONY: lint
lint:
	flake8 $(PACKAGE_DIR)

.PHONY: test
test:
	python3 setup.py test

.PHONY: tox
tox:
	tox

.PHONY: build
build:
	python3 setup.py build

.PHONY: install
install: build
	python3 setup.py install

.PHONY: install-user
install-user: build
	python3 setup.py install --user

.PHONY: git
git:
	git push --all
	git push --tags

.PHONY: check
check:
	python3 setup.py check

.PHONY: docs
docs:
	python3 -m sphinx.ext.apidoc -d 6 -e -f -o docs . *.py tests
	make -C docs clean html

.PHONY: docker
docker: docker_build docker_publish

.PHONY: docker_build
docker_build:
	docker build $(DOCKER_BUILD_ARGS) -t $(IMAGE_REGISTRY)/$(IMAGE_NAME):${RELEASE_VERSION} .

.PHONY: docker_publish
docker_publish:
	docker push $(IMAGE_REGISTRY)/$(IMAGE_NAME):$(RELEASE_VERSION)

.PHONY: release
release:
	git diff-index --quiet HEAD || { echo "untracked files! Aborting"; exit 1; }
	git checkout develop
	git checkout -b release/$(shell date +'%Y%m%d')
	git push origin release/$(shell date +'%Y%m%d')

.PHONY: db_upgrade
db_update:
	alembic revision --autogenerate -m "${MESSAGE}"
	alembic upgrade head
