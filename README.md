# TinyCloud - URL Shortener

A Flask-based URL shortener service with PostgreSQL database, Docker containerization, and Kubernetes deployment support.

## Features

- URL shortening with custom slugs
- RESTful API endpoints
- PostgreSQL database integration
- Docker containerization
- Kubernetes/Helm deployment
- Database migrations with Alembic

## Quick Start

### Using Docker Compose

1. Set up environment variables by copying the example file:
```bash
cp env.example .env
```

2. Edit the `.env` file with your desired values:
```bash
# Database Configuration
POSTGRES_USER=tinycloud
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=tinycloud

# Application Configuration
FLASK_ENV=development
```

3. Run the application:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - Health check
- `GET /url-mapping/` - List all URL mappings
- `GET /url-mapping/<id>` - Get specific URL mapping
- `POST /url-mapping/` - Create new URL mapping
- `PUT /url-mapping/<id>` - Update URL mapping
- `DELETE /url-mapping/<id>` - Delete URL mapping

## Development

### Prerequisites

- Python 3.13+
- PostgreSQL
- Docker (optional)

### Local Development

1. Install dependencies:
```bash
cd api/tinycloud
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp ../env.example ../.env
# Edit the .env file with your database credentials
```

3. Run the application:
```bash
export DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}
python app.py
```

## Deployment

### Kubernetes/Helm

```bash
helm install tinycloud charts/tinycloud/
```

## Project Structure

```
tinycloud-project/
├── api/tinycloud/          # Flask application
│   ├── models/            # SQLAlchemy models
│   ├── routes/            # API routes
│   ├── schemas/           # Marshmallow schemas
│   ├── extensions/        # Flask extensions
│   └── migrations/        # Database migrations
├── charts/tinycloud/      # Helm chart
└── docker-compose.yml     # Local development
```
