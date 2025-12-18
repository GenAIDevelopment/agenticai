# FastMCP API Demo

## Docker Compose Setup

### Start the application
```bash
docker-compose up -d
```

### Stop the application
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

## Direct Execution

### Install dependencies
```bash
uv sync
```

### Run with uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Access

- **Container**: http://localhost:18000
- **Direct**: http://localhost:8000