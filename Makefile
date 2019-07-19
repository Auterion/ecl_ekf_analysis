.PHONY:	build-container
	docker-compose build

.PHONY:	lint
lint:	build-container
	docker-compose run -e PYTHONDONTWRITEBYTECODE=1 --rm development /app/run_pylint.sh

.PHONY:	test
test:	build-container
	docker-compose run -e PYTHONDONTWRITEBYTECODE=1 --rm development [ -n "$$(find . -name __pycache__)" ] && find . -name __pycache__ | xargs rm -r || true
	docker-compose run -e PYTHONDONTWRITEBYTECODE=1 --rm development pytest -n 0 -v -p no:cacheprovider /app/tests/

.PHONY: analyse-file
analyse-file: build-container
	docker-compose run -e PYTHONDONTWRITEBYTECODE=1 -v $${file%/*}:$${file%/*} --rm development bash -c "python src/ecl_ekf_analysis/process_logdata_ekf.py $(file)"

.PHONY: analyse-dir
analyse-dir: build-container
	docker-compose run -it -e PYTHONDONTWRITEBYTECODE=1 -v $(dir):$(dir) --rm development bash -c "python src/ecl_ekf_analysis/batch_process_logdata_ekf.py $(dir) --overwrite"
