.PHONY: install
install:
	uv tool install --editable .

.PHONY: devinstall
devinstall:
	uv sync --frozen

.PHONY: test
test:
	uv run --frozen pytest -s tests

.PHONY: typecheck
typecheck:
	uv run --frozen mypy

.PHONY: testserver
testserver: test
	cd tests/out && python3 -m http.server

.PHONY: demo
demo:
	uv run --frozen mdsite --config demo.yaml

.PHONY: demoserver
demoserver: demo
	cd docs && python3 -m http.server
