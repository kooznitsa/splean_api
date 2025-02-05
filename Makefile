include .env

DOCKER_COMPOSE := docker compose --profile
DOCKER_EXEC := docker exec $(APP_NAME)_backend
DOCKER_PROFILE ?= main
MANAGE = poetry run python manage.py
DJANGOAPP ?= ''
MGRNAME ?= ''
FIXNAME ?= ''
TEST_DIR ?= ''
TXTPATH ?= '/home/app/common/tests/files/'

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


# -------------- DJANGO --------------

# Create an app. Example: make startapp DJANGOAPP=album
.PHONY: startapp
startapp:
	$(DOCKER_EXEC) $(MANAGE) startapp $(DJANGOAPP)

# Create superuser
.PHONY: createsuperuser
createsuperuser:
	$(DOCKER_EXEC) $(MANAGE) createsuperuser --noinput


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
# FIXNAME options: albums, songs. Example: make fixture FIXNAME=albums
.PHONY: fixture
fixture:
	$(DOCKER_EXEC) $(MANAGE) loaddata $(FIXNAME)

.PHONY: fixture-lines
fixture-lines:
	for filename in $$(ls -v line/fixtures/); do \
	  make fixture FIXNAME=$$filename; \
	done

# Loads all fixtures
.PHONY: allfixtures
allfixtures:
	make fixture FIXNAME=albums
	make fixture FIXNAME=songs
	make fixture-lines

# Creates JSON files with lines
.PHONY: createlinesjson
createlinesjson:
	$(DOCKER_EXEC) $(MANAGE) createlinesjson --path=$(TXTPATH)


# -------------- ELASTICSEARCH --------------

# Creates and populates the Elasticsearch index and mapping
.PHONY: elastic
elastic:
	$(DOCKER_EXEC) $(MANAGE) search_index --rebuild


# -------------- LINTER --------------

# Creates and populates the Elasticsearch index and mapping
.PHONY: linter
linter:
	$(DOCKER_EXEC) poetry run flake8 --max-line-length 119 --exclude line/lists/stop_words.py


# -------------- TESTS --------------

# Runs tests
# TEST_DIR options: album/tests, song/tests, line/tests. Example: make test TEST_DIR=song/tests
.PHONY: test
test:
	$(DOCKER_EXEC) poetry run pytest $(TEST_DIR) -v
