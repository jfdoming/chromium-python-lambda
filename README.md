# chromium-python-lambda
Base repository building AWS Lambda layers for Python-based web scrapers.

## Background
AWS Lambda lets you upload .zip files called "layers" which are free to store (versus a Docker image which is not free to store). This repository includes all dependencies and logic needed to build layers that you can upload to your lambda to enable Python access via Selenium.

## Usage
1. Ensure you have `make`, `curl`, and `jq` installed. (`docker` is required if you want to test locally.)
1. Clone the repository locally.
1. Run `make layers` from the root directory. Layers to upload will be populated in `layers/`.
