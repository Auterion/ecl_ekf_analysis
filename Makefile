.PHONY:	build-container
	docker-compose build

.PHONY:	lint
lint:	build-container
	docker-compose run -e PYTHONDONTWRITEBYTECODE=1 --rm development /app/run_pylint.sh

.PHONY:	test
test:	build-container
	docker-compose run -e PYTHONDONTWRITEBYTECODE=1 --rm development pytest -v --cache-clear


.PHONY: protos
protos:
	docker-compose build
	docker-compose run -e PYTHONDONTWRITEBYTECODE=1 --rm -u $$(id -u):$$(id -g) -v $$PWD/protos:/proto-source -v $$PWD/src/ecl_ekf_analysis/grpc_interfaces/:/proto-out development bash -c "python -m grpc_tools.protoc -I /proto-source --grpc_python_out=/proto-out --python_out=/proto-out google_protobuf_wrappers_cp.proto check_data.proto"
	sed -r -i 's/^import ([^. ]+_pb2)/import grpc_interfaces.\1/' src/ecl_ekf_analysis/grpc_interfaces/*.py