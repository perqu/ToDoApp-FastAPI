# Zmienne
PYTHON = python
PIP = pip
PROJECT_NAME = ToDoApp

# Cele
.PHONY: install run test lint format

install:
	$(PIP) install --upgrade $(PIP) &&\
		$(PIP) install -r requirements.txt

run:
	uvicorn main:app --reload --host localhost --port 8000

lint:
	pylint *.py --exit-zero

format:
	black *.py

all: lint format install