.PHONY: entorno regulatorio vigencia extraer verificar build test lint limpiar

entorno:
	uv pip install --python .venv/bin/python -r requirements.txt

regulatorio:
	PYTHONPATH=src .venv/bin/python -m renovable regulatorio

vigencia:
	PYTHONPATH=src .venv/bin/python -m renovable vigencia

extraer:
	PYTHONPATH=src .venv/bin/python -m renovable extract

extraer-fresco:
	PYTHONPATH=src .venv/bin/python -m renovable extract --refrescar

verificar:
	PYTHONPATH=src .venv/bin/python -m renovable verificar

build:
	PYTHONPATH=src .venv/bin/python -m renovable build

test:
	PYTHONPATH=src .venv/bin/python -m pytest -q

lint:
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .
