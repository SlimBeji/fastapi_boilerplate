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

lint: isort black

run:
	docker-compose down
	docker-compose up

build:
	docker-compose build
