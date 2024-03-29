#################### Variables ############################

# OS variables
# https://stackoverflow.com/questions/714100/os-detecting-makefile
ifeq ($(OS),Windows_NT)
	# Windows does not support uname command
    os_name := Windows
else
    os_name := $(shell uname -s)
	ifeq ($(os_name), Linux)
		open-browser := nohup xdg-open
		log-redirection := > /dev/null 2>&1
	else ifeq ($(os_name), Darwin)
		open-browser := open
	endif
endif

# Dev variables
dev-urls := http://localhost:5000/ http://localhost:5000/docs http://localhost:5001/redis:6379/0/ http://localhost:5050

#################### Commands ############################

# Dev commands
pages:
ifeq ($(os_name), Windows_NT)
	echo Not Implemented in Windows
else
	for url in $(dev-urls) ; do \
	eval '$(open-browser) $$url $(log-redirection)' ; \
	done
endif

isort:
	isort .

black:
	python -m black .

autoflake:
	autoflake -r --in-place --remove-all-unused-imports --exclude=**/models/__init__.py  ./

lint: isort black autoflake

fix-permission:
# Files genated withing docker have root permission
# linting command will fail because of permissions
# so using the chown command to fix the problem
	sudo chown -R slim:slim ./

# DB comands
dump-db:
	sudo rm -rf db/

init-aerich:
	docker exec -it postman-app aerich init -t backend.config.aerich_config

init-db:
	docker exec -it postman-app aerich init-db

migrate-db: init-aerich
	docker exec -it postman-app aerich migrate --name $(name)

upgrade-db:
	docker exec -it postman-app aerich upgrade

seed-db:
	docker exec -it postman-app python -m backend.scripts.seed_db

create-db: init-aerich init-db seed-db

recreate-db: init-aerich upgrade-db seed-db

# Docker commands
run:
	docker-compose down
	docker-compose up

build:
	docker-compose build

test:
	docker exec -it postman-app pytest
