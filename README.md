# TinyCloud Backend

## What Is This

This repository contains the TinyCloud backend: a Flask REST API for creating, listing, updating, deleting, and resolving short links.

It is the system of record for URL mappings and also exposes Prometheus metrics. The service runs locally with Docker Compose and is packaged for Kubernetes with Helm.

## How To Run

### Local development with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Local endpoints:

- Frontend: `http://localhost`
- Backend API: `http://localhost:8080`
- Postgres: `localhost:5432`

The compose setup expects the frontend repository to exist next to this one at `../tinycloud-frontend`.

### Manual migration commands

Migrations are applied on startup via `run.sh`, but they can also be run manually:

```bash
docker exec -it <container> flask db migrate -m "describe change"
docker exec -it <container> flask db upgrade
```

### Example request

```bash
curl -X POST http://localhost:8080/url-mapping/ \
  -H "Content-Type: application/json" \
  -d '{"long_url":"https://example.com"}'
```

## Architecture

Main runtime pieces:

- Flask app factory in `api/tinycloud/app.py`
- HTTP routes in `api/tinycloud/routes/url_mapping.py`
- SQLAlchemy model in `api/tinycloud/models/url_mapping.py`
- Marshmallow schemas in `api/tinycloud/schemas`
- Prometheus instrumentation in `api/tinycloud/services/metrics.py`
- Optional Elasticsearch client wiring in `api/tinycloud/services/elasticsearch_service.py`
- PostgreSQL as the primary datastore
- Helm chart in `charts/tinycloud-backend`

Request flow:

1. The frontend or any client calls `/url-mapping/...`.
2. Flask validates input and loads/saves `UrlMapping` records in Postgres.
3. Redirect requests resolve the stored `short_url` and return HTTP redirect responses.
4. `/metrics` exposes app and host metrics for Prometheus scraping.

## CI/CD

GitHub Actions workflow: `.github/workflows/pipeline.yml`

On every push to `main`, the pipeline:

1. Creates a new patch semver tag.
2. Builds the Docker image.
3. Pushes the image to Amazon ECR.
4. Packages and pushes the Helm chart to ECR as an OCI artifact.
5. Triggers `tinycloud-infra` to deploy the new backend version to `dev`.

## Infra / Deploy Flow

Deployment is split across repositories:

1. This repo builds and publishes the backend image and chart.
2. `tinycloud-infra` receives the version and target environment.
3. Helmfile in `tinycloud-infra/charts/helmfile.yaml.gotmpl` selects the backend release for `dev`, `staging`, or `prod`.
4. Environment-specific values provide ingress hostnames, secrets, resource limits, and Postgres settings.
5. Kubernetes pulls the image from ECR and rolls the workload.

Manual deploy example:

```bash
helmfile --environment dev \
  -l name=tinycloud-backend-dev \
  --state-values-set version=<version> \
  sync --wait
```

## What Was Learned

- A small CRUD API becomes much easier to operate once packaging, migrations, metrics, and deployment are treated as first-class concerns.
- Keeping Helm packaging in the app repo and actual rollout logic in the infra repo creates a clean separation between delivery and operations.
- Exposing `/metrics` early makes it much easier to wire monitoring later without changing the public API.

## Known Limitations

- Short code generation is random and retry-based; there is no custom aliasing or deterministic strategy yet.
- The API currently returns the full list of mappings without pagination, filtering, or search.
- Elasticsearch is wired in configuration, but search is not part of the main request flow yet.
- Docker Compose local startup depends on the frontend repo being checked out as a sibling directory.
