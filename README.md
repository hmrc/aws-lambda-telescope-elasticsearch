# aws-lambda-telescope-elasticsearch

[![Brought to you by Telemetry Team](https://img.shields.io/badge/MDTP-Telemetry-40D9C0?style=flat&labelColor=000000&logo=gov.uk)](https://confluence.tools.tax.service.gov.uk/display/TEL/Telemetry)

Telescope Elasticsearch queries the elastic API and derives metrics that are then sent to clickhouse.

Please check the [telemetry-terraform](https://github.com/hmrc/telemetry-terraform) repository for details on how this Lambda is deployed.

## Requirements

* [Python 3.8+](https://www.python.org/downloads/release)
* [Poetry](https://python-poetry.org/)

## Quick start

```shell
# Install correct version of Python
pyenv install $(cat .python-version)

# Optional set up environment variables
export POETRY_VIRTUALENVS_IN_PROJECT=true
export PYTHONPATH=/home/james/hmrcDev/aws-lambda-telescope-elasticsearch
export MDTP_ENVIRONMENT=integration

# Run tests:
make test

# Package the lambda locally:
make package
```

### Environment variables
The following environment variables are processed by the lambda handler and can therefore be set in Terraform to
override the defaults provided:

* `lambda_name` (default: "telescope-elasticsearch")
* `log_level` (default: "INFO")

### License

This code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").

# References

### License

This code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").
