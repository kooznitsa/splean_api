include .env

DOCKER_COMPOSE := docker compose --profile
DOCKER_EXEC := docker exec -it $(APP_NAME)_backend
DOCKER_PROFILE ?= main
MANAGE = poetry run python manage.py
MGRNAME ?= ''

# -------------- DOCKER --------------

# Runs php and database containers
# DOCKER_PROFILE options: main, secondary. Example: make run DOCKER_PROFILE=main
.PHONY: run
run:
	$(DOCKER_COMPOSE) $(DOCKER_PROFILE) up -d --build

# Removes php and database containers
# DOCKER_PROFILE options: main, secondary. Example: make stop DOCKER_PROFILE=main
.PHONY: stop
stop:
	$(DOCKER_COMPOSE) $(DOCKER_PROFILE) down

# Enters PHP container
.PHONY: entercontainer
entercontainer:
	$(DOCKER_EXEC) sh


# -------------- MIGRATIONS --------------

# Create a migration file specifying filename. Example: make makemigrations MGRNAME=create_albums_songs_lines
.PHONY: makemigrations
makemigrations:
	$(DOCKER_EXEC) $(MANAGE) makemigrations --name $(MGRNAME)

# Applies migration
.PHONY: migrate
migrate:
	$(DOCKER_EXEC) $(MANAGE) migrate


# -------------- DATABASE --------------

# Loads fixture
# FIXNAME options: albums, songs, lines. Example: make fixture FIXNAME=albums
.PHONY: fixture
fixture:
	$(DOCKER_EXEC) $(MANAGE) loaddata $(FIXNAME)


# -------------- ELASTICSEARCH --------------

# Creates and populates the Elasticsearch index and mapping
.PHONY: elastic
elastic:
	$(DOCKER_EXEC) $(MANAGE) search_index --rebuild


# -------------- LINTER --------------

# Creates and populates the Elasticsearch index and mapping
.PHONY: linter
linter:
	poetry run flake8
