# Makefile for Fitness AI Agent Docker Operations

.PHONY: help build up down logs restart clean test

# Default target
help:
	@echo "Fitness AI Agent - Docker Commands"
	@echo "===================================="
	@echo ""
	@echo "Development:"
	@echo "  make build       - Build all Docker images"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View logs (all services)"
	@echo "  make logs-backend  - View backend logs"
	@echo "  make logs-frontend - View frontend logs"
	@echo ""
	@echo "Production:"
	@echo "  make prod-build  - Build production images"
	@echo "  make prod-up     - Start production services"
	@echo "  make prod-down   - Stop production services"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean       - Remove containers and volumes"
	@echo "  make clean-all   - Remove everything (containers, volumes, images)"
	@echo "  make ps          - Show running containers"
	@echo "  make stats       - Show resource usage"
	@echo ""
	@echo "Testing:"
	@echo "  make test        - Run tests in backend container"
	@echo "  make shell-backend  - Open shell in backend container"
	@echo "  make shell-frontend - Open shell in frontend container"
	@echo ""
	@echo "Ollama:"
	@echo "  make ollama-up   - Start with Ollama service"
	@echo "  make ollama-pull - Pull Ollama model (llama3.2)"

# Development commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

# Production commands
prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-up:
	docker-compose -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

# Maintenance commands
clean:
	docker-compose down -v

clean-all:
	docker-compose down -v --rmi all
	docker system prune -f

ps:
	docker-compose ps

stats:
	docker stats

# Testing commands
test:
	docker-compose exec backend pytest tests/

shell-backend:
	docker-compose exec backend /bin/bash

shell-frontend:
	docker-compose exec frontend /bin/bash

# Ollama commands
ollama-up:
	docker-compose --profile ollama up -d

ollama-pull:
	docker-compose exec ollama ollama pull llama3.2

# Quick rebuild and restart
rebuild:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

# View health status
health:
	@echo "Backend health:"
	@curl -s http://localhost:8000/api/health | python -m json.tool || echo "Backend not responding"
	@echo ""
	@echo "Frontend health:"
	@curl -s http://localhost:8501/_stcore/health || echo "Frontend not responding"
