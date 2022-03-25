
.PHONY: build

isort:
	poetry run isort .

black:
	poetry run black .

build:
	docker-compose -f app.yml build

run: build
	docker-compose -f app.yml up

format: isort black
