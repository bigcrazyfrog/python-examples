# Python examples

Small projects combined into one repository.

## Installation

You have to have the following tools installed prior initializing the project:

- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

### Create virtualenv

```bash
pyenv virtualenv-delete --force python-examples
pyenv install 3.11 --skip-existing
pyenv virtualenv `pyenv latest 3.11` python-examples
pyenv local python-examples
pyenv activate python-examples
```

### Install requirements (linters, pytest)

Install requirements
```bash
pip install -r requirements.txt
```

### Install linter for your commits messages

```bash
gitlint install-hook
```

## How to check code style

Check all:
```bash
bash style.sh
```

Fix imports:
```bash
isort .
```

## Run tests

```bash
bash tests.sh
```
