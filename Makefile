dev-deps:
	@echo "Compiling and Installing dev-requirements.txt..."
	@uv pip compile requirements.in dev-requirements.in -o dev-requirements.txt
	@uv pip install -r dev-requirements.txt

deps:
	@echo "Compiling and Installing requirements.txt..."
	@uv pip compile requirements.in -o requirements.txt
	@uv pip install -r requirements.txt

up:
	@echo "Starting the server..."
	@docker compose up -d

build:
	@echo "Building the server..."
	@docker compose build

stop:
	@echo "Killing the server..."
	@docker compose stop

down:
	@echo "Stopping the server..."
	@docker compose down

ruff:
  # Run ruff checks
	ruff check --fix
	ruff format
