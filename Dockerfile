FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    python3-psycopg2 \
    gcc \
    g++ \
    musl-dev \
    binutils \
    gdal-bin \
    python3-gdal \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY . /app

RUN chmod +x /app/entrypoints/server.sh
RUN chmod +x /app/entrypoints/beat.sh
RUN chmod +x /app/entrypoints/worker.sh
RUN chmod +x /app/entrypoints/daphne.sh
RUN chmod +x /app/entrypoints/*.sh


COPY ./requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn uvicorn websockets


EXPOSE 8000

CMD [ "/app/entrypoints/server.sh" ]

