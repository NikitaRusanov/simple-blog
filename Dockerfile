FROM python:3.12.1-slim-bookworm

WORKDIR /app

COPY poetry.lock pyproject.toml ./

ENV POETRY_VIRTUALENVS_CREATE=false 

RUN pip install poetry && poetry install

COPY certs ./certs

COPY src ./src

WORKDIR /app/src

EXPOSE 80

ENTRYPOINT [ "uvicorn", "main:app"]

CMD [ "--host", "0.0.0.0", "--port", "80" ]