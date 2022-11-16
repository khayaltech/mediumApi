build:
	docker compose -f compose-local.yml up --build -d --remove-orphans

up:
	docker compose -f compose-local.yml up -d

down:
	docker compose -f compose-local.yml down

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





