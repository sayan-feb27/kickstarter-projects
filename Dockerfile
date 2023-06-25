FROM python:3.10

ARG REQUIREMENTS_FILE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements/ /code/requirements/

RUN #apk update
RUN #apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --no-cache-dir --upgrade -r /code/requirements/$REQUIREMENTS_FILE

COPY . /code
COPY pyproject.toml /code/pyproject.toml
