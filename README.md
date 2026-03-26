# TinyCloud - URL Shortener

Flask REST API for URL shortening. Backed by PostgreSQL, containerized with Docker, deployed to Kubernetes via Helm.

---

## Getting Started

```bash
cp .env.example .env
# fill in DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT
```

### Run with Docker Compose

```bash
docker compose up --build
```

| Service  | URL                   |
|----------|-----------------------|
| Frontend | http://localhost      |
| API      | http://localhost:8080 |
| Postgres | localhost:5432        |

> Requires [tinycloud-frontend](../tinycloud-frontend) in the parent directory.

---

## Database Migrations

Migrations run automatically on startup. To manage them manually:

```bash
docker exec -it <container> flask db migrate -m "description"
docker exec -it <container> flask db upgrade
```

---

## API

| Method | Endpoint                   | Description          |
|--------|----------------------------|----------------------|
| GET    | `/`                        | Health check         |
| GET    | `/url-mapping/`            | List all mappings    |
| POST   | `/url-mapping/`            | Create short URL     |
| GET    | `/url-mapping/<short_url>` | Redirect to long URL |
| PUT    | `/url-mapping/<id>`        | Update mapping       |
| DELETE | `/url-mapping/<id>`        | Delete mapping       |
| GET    | `/metrics`                 | Prometheus metrics   |

**Create a short URL:**

```bash
curl -X POST http://localhost:8080/url-mapping/ \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com"}'
```

---

## Build & Push

```bash
# Build image
docker build --no-cache -t tinycloud-backend:latest .

# Tag and push to ECR
docker tag tinycloud-backend:latest <registry>/tinycloud-docker-backend:<version>
docker push <registry>/tinycloud-docker-backend:<version>

# Package and push Helm chart
helm dependency update charts/tinycloud-backend
helm package charts/tinycloud-backend --version <version>
helm push tinycloud-backend-*.tgz oci://<registry>
```

---

## Deployment

Deployed via [helmfile](https://helmfile.readthedocs.io/) from the [tinycloud-infra](https://github.com/cherya05/tinycloud-infra) repo.

```bash
helmfile --environment dev \
  -l name=tinycloud-backend-dev \
  --state-values-set version=<version> \
  sync --wait
```

Environments: `dev` · `staging` · `prod`

Values per environment: `charts/tinycloud-backend/values-{env}.yaml`

---

## CI/CD

Pushing to `main` triggers the pipeline automatically:

1. Bumps semver tag
2. Builds and pushes Docker image to ECR
3. Packages and pushes Helm chart to ECR
4. Triggers deployment to `dev` via `tinycloud-infra` pipeline
