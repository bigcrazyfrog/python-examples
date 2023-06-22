FROM python:3.11.3-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY duplicate_scanner.py entities.py plushkin.py /code/

ENTRYPOINT [ "python3", "plushkin.py"]
