# FastMCP HTTP Server

A Model Context Protocol (MCP) server implementation using FastAPI.

## Docker Setup

### Build the Docker Image

```bash
docker build -t fastmcp-http .
```

### Run the Container

```bash
docker run -p 8000:8000 fastmcp-http
```

The server will be available at `http://localhost:8000`

### Environment Variables

- `MCP_HOST`: Host to bind to (default: "0.0.0.0")
- `MCP_PORT`: Port to bind to (default: 8000)

### Custom Port Example

```bash
docker run -p 3000:3000 -e MCP_PORT=3000 fastmcp-http
```