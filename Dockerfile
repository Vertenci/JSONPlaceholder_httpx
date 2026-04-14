FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN pip install --no-cache-dir uvloop httptools

COPY . .

RUN chmod +x docker-entrypoint.sh docker-entrypoint.prod.sh

EXPOSE 8000

CMD ["/bin/bash", "docker-entrypoint.sh"]
