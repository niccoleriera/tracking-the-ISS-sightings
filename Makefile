NAME ?= niccoleriera

all: build run

build:
	docker build -t ${NAME}/flask-isstracker .
run:
	docker run -d -p 5022:5000 ${NAME}/flask-isstracker:latest
push:
	docker push ${NAME}/flask-isstracker:latest
