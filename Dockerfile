FROM python:3.12-slim-bullseye

WORKDIR /app

COPY poetry.lock pyproject.toml ./

ENV POETRY_VIRTUALENVS_CREATE=false 

RUN pip install poetry && poetry install

COPY src ./

EXPOSE 80

ENTRYPOINT [ "uvicorn", "main:app"]

CMD [ "--host", "0.0.0.0", "--port", "80" ]