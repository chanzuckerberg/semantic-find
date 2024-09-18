## Installation
First create a python virtual environment with `python3 -m venv .venv` or `virtualenv -p python3 .venv`. 

Activate the environment with `source .venv/bin/activate`. 

Install the python dependencies with `make install` or `pip install '.[dev]'`

Initialize the database with `make up`. It takes 10 seconds to wait for the docker container to come up. 

To load the database run `make load`. On the first run it takes a while for the model to download and initialize. 

Run a query with: `python3 src/semantic_find/cli.py search "Tell me about potatoes"`. 

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](https://github.com/chanzuckerberg/.github/blob/master/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [opensource@chanzuckerberg.com](mailto:opensource@chanzuckerberg.com).

## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@chanzuckerberg.com](mailto:security@chanzuckerberg.com).
