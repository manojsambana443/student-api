
IMAGE_NAME=student-api
VERSION=1.2.0

.PHONY: install run test migrate docker-build docker-run setup down logs status

install:
	pip install -r requirements.txt

run:
	python app.py

test:
	pytest

migrate:
	python migrate.py

docker-build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

docker-run:
	docker run --rm -p 5000:5000 \
		--add-host=host.docker.internal:host-gateway \
		--env-file .env \
		-e DB_HOST=host.docker.internal \
		$(IMAGE_NAME):$(VERSION)

setup:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

status:
	docker compose ps -a
