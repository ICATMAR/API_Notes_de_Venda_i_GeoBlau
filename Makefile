.PHONY: help build up down restart logs shell migrate makemigrations createsuperuser test coverage lint format security-check clean

help:  ## Mostra aquesta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build:  ## Construeix les imatges Docker
	docker-compose build

up:  ## Inicia els contenidors
	docker-compose up -d

down:  ## Atura els contenidors
	docker-compose down

restart:  ## Reinicia els contenidors
	docker-compose restart

logs:  ## Mostra els logs
	docker-compose logs -f

logs-api:  ## Mostra només els logs de l'API
	docker-compose logs -f api

shell:  ## Obre una shell dins el contenidor de l'API
	docker-compose exec api /bin/bash

shell-db:  ## Obre una shell PostgreSQL
	docker-compose exec db psql -U vcpe_user -d vcpe_db

migrate:  ## Executa les migracions
	docker-compose exec api python manage.py migrate

makemigrations:  ## Crea noves migracions
	docker-compose exec api python manage.py makemigrations

createsuperuser:  ## Crea un superusuari
	docker-compose exec api python manage.py createsuperuser

test:  ## Executa els tests
	docker-compose exec api pytest

test-unit:  ## Executa només els tests unitaris
	docker-compose exec api pytest -m unit

test-integration:  ## Executa només els tests d'integració
	docker-compose exec api pytest -m integration

test-security:  ## Executa només els tests de seguretat
	docker-compose exec api pytest -m security

coverage:  ## Genera informe de cobertura
	docker-compose exec api pytest --cov --cov-report=html
	@echo "Informe generat a htmlcov/index.html"

lint:  ## Executa linters (flake8, mypy)
	docker-compose exec api flake8 . --max-line-length=120 --extend-ignore=E203,W503
	docker-compose exec api mypy .

format:  ## Formata el codi amb black i isort
	docker-compose exec api black .
	docker-compose exec api isort .

security-check:  ## Comprova vulnerabilitats de seguretat
	docker-compose exec api bandit -r . -c pyproject.toml
	docker-compose exec api safety check

pre-commit-install:  ## Instal·la els hooks de pre-commit
	pre-commit install

pre-commit-run:  ## Executa pre-commit en tots els fitxers
	pre-commit run --all-files

collectstatic:  ## Recull fitxers estàtics
	docker-compose exec api python manage.py collectstatic --noinput

clean:  ## Neteja fitxers temporals
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

setup:  ## Configuració inicial del projecte
	cp .env.example .env
	@echo "Edita el fitxer .env amb les teves configuracions"
	@echo "Després executa: make build && make up && make migrate"

init-dev:  ## Inicialitza entorn de desenvolupament
	make build
	make up
	sleep 10
	make migrate
	@echo "Entorn de desenvolupament inicialitzat!"
	@echo "Crea un superusuari amb: make createsuperuser"

backup-db:  ## Fa backup de la base de dades
	docker-compose exec -T db pg_dump -U vcpe_user vcpe_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup creat: backup_$(shell date +%Y%m%d_%H%M%S).sql"

restore-db:  ## Restaura un backup (usa: make restore-db FILE=backup.sql)
	docker-compose exec -T db psql -U vcpe_user vcpe_db < $(FILE)

check-security:  ## Executa Django security check
	docker-compose exec api python manage.py check --deploy

docs:  ## Genera documentació de l'API
	docker-compose exec api python manage.py spectacular --file schema.yml
	@echo "Esquema OpenAPI generat: schema.yml"

api-docs:  ## Obre la documentació interactiva de l'API
	@echo "Documentació disponible a: http://localhost:8000/api/docs/"

monitor:  ## Mostra estadístiques dels contenidors
	docker stats
