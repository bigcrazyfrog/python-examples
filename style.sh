set -xe
isort examples --check-only
flake8 examples --show-source
pylint examples
mypy examples
