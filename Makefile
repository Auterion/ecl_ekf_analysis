.PHONY:	build-container
	docker-compose build

.PHONY:	lint
lint:	build-container
	docker-compose run -e PYTHONDONTWRITEBYTECODE=1 --rm development /app/run_pylint.sh

.PHONY:	test
test:	build-container
	docker-compose run -e PYTHONDONTWRITEBYTECODE=1 --rm development pytest -v --cache-clear