.PHONY: all typing style unit-tests ci-build

all: typing style unit-tests ci-build

ci-build: dependencies unit-tests typing style unused-imports imports-order

unit-tests:
		@echo "Running tests"
		python -W error:::redemptions[.*] -m unittest discover -v tests/unit
		@echo

dependencies:
		@echo "Installing newest dependencies"
		poetry install --no-root
		@echo

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
