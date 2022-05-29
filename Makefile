.PHONY: all typing style unit-tests ci-build

all: typing style unit-tests ci-build

ci-build: dependencies unit-tests typing style unused-imports imports-order

dependencies:
		@echo "Installing newest dependencies"
		poetry install --no-root
		@echo

unit-tests:
		@echo "Running tests"
		python -m unittest discover -v tests/unit
		@echo

integration-tests:
		@echo "Running tests"
		python -m unittest discover -v tests/integration
		@echo

acceptance-tests:
		@echo "Running acceptance tests"
		python -m unittest discover -v tests/acceptance
		@echo

run-server:
	uvicorn src.main.web:create_app --host "127.0.0.1"  --port 8080 --log-level info

typing:
		@echo "Checking typing"
		pyright
		@echo

style:
		@echo "Checking style"
		black --check .
		@echo

unused-imports:
		@echo "Checking unused imports"
		autoflake --check -r --remove-all-unused-imports .
		@echo

imports-order:
		@echo "Checking imports order"
		isort . --check
		@echo

reformat:
		@echo "Running autoformatter and cleaners"
		autoflake -i -r --remove-all-unused-imports .
		isort .
		black .
		@echo
