FROM python:3.11-buster as poetry
ENV POETRY_VERSION=1.5.1
RUN curl -sSL https://install.python-poetry.org | python
WORKDIR /app

FROM python:3.11-buster as venv
COPY --from=poetry /root/.local /root/.local
ENV PATH /root/.local/bin:$PATH
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN python -m venv --copies /app/venv && \
    . /app/venv/bin/activate && \
    poetry install --no-root

FROM python:3.11-slim-buster as prod
WORKDIR /app
COPY --from=venv /app/venv /app/venv/
ENV PATH /app/venv/bin:$PATH
COPY ./fly_sse_example /app/fly_sse_example
CMD ["uvicorn", "fly_sse_example.main:app", "--host", "0.0.0.0", "--port", "8080"]