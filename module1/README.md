# Data Engineering Zoomcamp (DataTalksClub) — Module 1 (Week 1)

This folder contains my work for **Module 1 / Week 1** of the **DataTalksClub Data Engineering Zoomcamp**.  
It focuses on Docker, Docker Compose, PostgreSQL + pgAdmin, and ingesting NYC TLC taxi data into Postgres.

## What’s inside

- `docker-compose.yaml`: starts `postgres` + `pgadmin`
- `ingest_data_yellow.py`: ingest Yellow taxi data into Postgres
- `ingest_data_green.py`: ingest Green taxi data (Parquet) into Postgres
- `zones_ingest.py`: ingest taxi zones lookup table into Postgres
- `homework.txt`: answers + SQL queries used in pgAdmin
- `Dockerfile.*`: Docker images used to run ingestion scripts

## Prerequisites

- Docker Desktop (Windows)
- Git

## Quickstart (Postgres + pgAdmin)

From this folder:

```bash
docker compose up -d
```

- **Postgres** is exposed on `localhost:6060` (container port is `5432`).
- **pgAdmin** is exposed on `localhost:8888`.

To stop:

```bash
docker compose down
```

## Ingestion (run as containers)

Build an image using the Dockerfile you want, then run it on the compose network (`homework_default`) so it can reach the `postgres` service by hostname.

Example (green):

```bash
docker build -f Dockerfile.greenHW -t taxi_green:v005 .
docker run -it --rm --network=homework_default taxi_green:v005 ^
  --pg-user=root --pg-pass=root --pg-host=postgres --pg-port=5432 ^
  --pg-db=data_talks_test --target-table=taxi_green_table
```

## Notes (Windows ports + volumes)

- If Docker fails to bind ports like 8080/8085 on Windows, it can be due to **reserved port ranges**. Using a port like `8888` often avoids this.
- Postgres data persistence depends on mounting the volume to the correct path:
  - Correct: `/var/lib/postgresql`

