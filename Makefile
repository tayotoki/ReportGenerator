build:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml build

up:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up

redis_up:
	docker-compose up redis

down:
	docker-compose down

exec_backend:
	docker-compose exec backend /bin/bash

test:
	docker-compose exec backend pytest --create-db

makemigrations:
	docker-compose exec backend python manage.py makemigrations

migrations_merge:
	docker-compose exec backend python manage.py makemigrations --merge

migrate:
	docker-compose exec backend python manage.py migrate


shell:
	docker-compose exec backend python manage.py shell
