# FastAPI CRUD Project Makefile

# Variables
DOCKER_COMPOSE = docker-compose
PROJECT_NAME = fastapi-crud

# Help
.PHONY: help
help: ## Mostra questo messaggio di aiuto
	@echo "FastAPI CRUD Project - Comandi disponibili:"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development
.PHONY: build
build: ## Costruisce i container Docker
	$(DOCKER_COMPOSE) build

.PHONY: up
up: ## Avvia tutti i servizi
	$(DOCKER_COMPOSE) up -d

.PHONY: down
down: ## Ferma tutti i servizi
	$(DOCKER_COMPOSE) down

.PHONY: restart
restart: ## Riavvia tutti i servizi
	$(DOCKER_COMPOSE) restart

.PHONY: logs
logs: ## Mostra i log di tutti i servizi
	$(DOCKER_COMPOSE) logs -f

.PHONY: logs-app
logs-app: ## Mostra i log dell'app FastAPI
	$(DOCKER_COMPOSE) logs -f fastapi

.PHONY: logs-db
logs-db: ## Mostra i log del database
	$(DOCKER_COMPOSE) logs -f postgres

# Database
.PHONY: db-shell
db-shell: ## Accede alla shell del database PostgreSQL
	$(DOCKER_COMPOSE) exec postgres psql -U postgres -d fastapi_db

.PHONY: db-backup
db-backup: ## Crea un backup del database
	@echo "Creando backup del database..."
	$(DOCKER_COMPOSE) exec postgres pg_dump -U postgres fastapi_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

.PHONY: db-reset
db-reset: ## Reset completo del database (ATTENZIONE: cancella tutti i dati)
	@echo "ATTENZIONE: Questo comando cancellerà tutti i dati del database!"
	@read -p "Sei sicuro? (y/N): " confirm && [ "$$confirm" = "y" ]
	$(DOCKER_COMPOSE) down -v
	docker volume rm $(PROJECT_NAME)_postgres_data 2>/dev/null || true
	$(DOCKER_COMPOSE) up -d

# Application
.PHONY: shell
shell: ## Accede alla shell del container FastAPI
	$(DOCKER_COMPOSE) exec fastapi /bin/bash

.PHONY: shell-root
shell-root: ## Accede alla shell del container FastAPI come root
	$(DOCKER_COMPOSE) exec -u root fastapi /bin/bash

.PHONY: install
install: ## Installa le dipendenze Python
	$(DOCKER_COMPOSE) exec fastapi pip install -r requirements.txt

.PHONY: test
test: ## Esegue i test
	$(DOCKER_COMPOSE) exec fastapi python -m pytest

# Monitoring
.PHONY: status
status: ## Mostra lo stato dei container
	$(DOCKER_COMPOSE) ps

.PHONY: stats
stats: ## Mostra le statistiche dei container
	docker stats $(shell $(DOCKER_COMPOSE) ps -q)

# Cleanup
.PHONY: clean
clean: ## Rimuove container, volumi e immagini non utilizzati
	$(DOCKER_COMPOSE) down -v --rmi all
	docker system prune -f

.PHONY: clean-volumes
clean-volumes: ## Rimuove solo i volumi (ATTENZIONE: cancella tutti i dati)
	@echo "ATTENZIONE: Questo comando cancellerà tutti i dati persistenti!"
	@read -p "Sei sicuro? (y/N): " confirm && [ "$$confirm" = "y" ]
	$(DOCKER_COMPOSE) down -v

# URLs
.PHONY: urls
urls: ## Mostra gli URL di accesso ai servizi
	@echo "FastAPI CRUD Project - URL dei servizi:"
	@echo "  📱 App FastAPI:    http://localhost:8000"
	@echo "  🗄️  pgAdmin:       http://localhost:5050"
	@echo "  📊 API Docs:      http://localhost:8000/docs"
	@echo "  📋 API Redoc:     http://localhost:8000/redoc"
	@echo "  🌐 Caddy (prod):  http://localhost"

# Production
.PHONY: prod-up
prod-up: ## Avvia in modalità produzione
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d

.PHONY: prod-build
prod-build: ## Build per produzione
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml build

# Security
.PHONY: security-scan
security-scan: ## Scansiona le vulnerabilità di sicurezza
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
		-v $(PWD):/app \
		aquasec/trivy:latest fs /app

# Default target
.DEFAULT_GOAL := help