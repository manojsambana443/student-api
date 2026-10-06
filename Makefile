IMAGE_NAME=student-api
VERSION=1.1.0

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
