.PHONY: install
install:
	uv tool install --editable .

.PHONY: devinstall
devinstall:
	uv sync

.PHONY: test
test:
	uv run pytest -s tests

.PHONY: testserver
testserver: test
	cd tests/out && python3 -m http.server

.PHONY: demo
demo:
	uv run mdsite --config demo.yaml

.PHONY: demoserver
demoserver: demo
	cd docs && python3 -m http.server
