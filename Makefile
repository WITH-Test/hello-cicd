
.PHONY: build

build:
	docker-compose -f app.yml build

run: build
	docker-compose -f app.yml up
