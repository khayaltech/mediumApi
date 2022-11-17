build:
	docker compose -f compose-local.yml up --build -d --remove-orphans

up:
	docker compose -f compose-local.yml up

down:
	docker compose -f compose-local.yml down

config:
	docker compose -f compose-local.yml config

show_logs:
	docker compose -f compose-local.yml logs

migrate:
	docker compose -f compose-local.yml run --rm api python3 manage.py migrate

makemigrations:
	docker compose -f compose-local.yml run --rm api python3 manage.py makemigrations

collectstatic:
	docker compose -f compose-local.yml run --rm api python3 manage.py collectstatic --no-input --clear

superuser:
	docker compose -f compose-local.yml run --rm api python3 manage.py createsuperuser


volume:
	docker volume inspect mediumapi_local_postgres_data

black:
	docker compose -f compose-local.yml exec api black --exclude=migrations --exclude=env .

isort:
	docker compose -f compose-local.yml exec api isort . --skip env --skip migrations


flake8:
	docker compose -f compose-local.yml exec api flake8 .
