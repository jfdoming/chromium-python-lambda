.PHONY: build@amd64 build@arm64 build-otp run run@arm64 run@amd64 layers layers/scraper_layer.zip call setup-symlinks help

run: run@arm64

run@amd64: .otp build@amd64
	@scripts/run_docker.sh amd64

run@arm64: .otp build@arm64
	@scripts/run_docker.sh arm64

run@layers: build@layers
	@scripts/run_docker.sh amd64

build@amd64: layers
	@docker build --platform linux/amd64 . -t python-scraper

build@arm64: layers
	@docker build --platform linux/arm64 -f Dockerfile.arm64.dev . -t python-scraper

build@layers: layers
	@docker build --platform linux/amd64 -f Dockerfile.layers . -t python-scraper


layers: layers/py_deps_layer.zip layers/chrome_layer.zip layers/scraper_layer.zip layers/chromedriver_local_libs_layer.zip

layers/py_deps_layer.zip: scripts/build_py_deps_layer.sh requirements.txt
	@scripts/build_py_deps_layer.sh

layers/chrome_layer.zip: scripts/build_chromium_layer.sh scripts/update_cd.sh
	@scripts/build_chromium_layer.sh

layers/chromedriver_local_libs_layer.zip: scripts/build_chromedriver_local_libs_layer.sh lib/*
	@scripts/build_chromedriver_local_libs_layer.sh

layers/scraper_layer.zip: scripts/build_scraper_layer.sh *.py scrape/* scrape/*/* scrape/*/*/*
	@scripts/build_scraper_layer.sh

test:
	@curl localhost/2015-03-31/functions/function/invocations -d "$$(cat $$PROJECT_ROOT/config.json)" 2>/dev/null | python3 local/pretty_output.py

call:
	@scripts/run_lambda.sh scraper_arn

setup-symlinks:
	@ln -snf "$$(realpath scrape/)" "$$PROJECT_ROOT"/scrape
	@ln -sf "$$(realpath requirements.txt)" "$$PROJECT_ROOT"/requirements.txt
	@ln -sf "$$(realpath dev-requirements.txt)" "$$PROJECT_ROOT"/dev-requirements.txt

help:
	@echo "Usage: make [build | run | test | layers | call | help]"
