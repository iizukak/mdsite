.PHONY: install
install:
	pip3 install -e .

.PHONY: devinstall
devinstall:
	pip3 install -e ".[dev]"

.PHONY: test
test:
	pytest -s tests

.PHONY: docs
docs: install
	cp ./README.md demo/in/index.md
	cd ./demo && potage
	cp -r ./demo/docs ./

.PHONY: demo
demo: docs
	cd docs && python3 -m http.server