.PHONY: watch deploy build

watch:
	@echo "Start watch"
	@while true; do \
		inotifywait -r -e modify,create,delete .; \
		echo "Changes detected"; \
		make deploy; \
	done

build:
	@echo "Docker-image start build"
	@GIT_HASH=$(shell git rev-parse --short HEAD) && \
	docker build -t tzb:$$GIT_HASH .

deploy: build
	@echo "Docker-container run"
	@GIT_HASH=$(shell git rev-parse --short HEAD) && \
	if docker ps -q -f name=tzb; then \
		docker stop tzb; \
		docker rm tzb; \
	fi; \
	docker run --name tzb -p 1488:1488 -d tzb:$$GIT_HASH
	@echo "Docker container started"

