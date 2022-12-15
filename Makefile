.PHONY: install
install:
	pip3 install -e .

.PHONY: devinstall
devinstall:
	pip3 install -e ".[dev]"

.PHONY: server
server:
	cd out && python3 -m http.server