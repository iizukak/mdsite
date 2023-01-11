.PHONY: install
install:
	pip3 install -e .

.PHONY: devinstall
devinstall:
	pip3 install -e ".[dev]"

.PHONY: test
test:
	pytest -s tests

.PHONY: testserver
testserver: test
	cd tests/out && python3 -m http.server

.PHONY: docs
docs:
	cp ./README.md demo/in/index.md
	cd ./demo && mdsite
	cp -r ./demo/docs ./

.PHONY: demo
demo: docs
	cd docs && python3 -m http.server
