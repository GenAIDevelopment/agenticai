## Curl Tests

### 1. Initialize MCP Connection

```bash
curl -s -X POST http://localhost:18000/mcp \
  -H "content-type: application/json" \
  -H "accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0", "id":1, "method":"initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
  }'
```

### 2. Complete Initialization

```bash
curl -s -X POST http://localhost:18000/mcp \
  -H "content-type: application/json" \
  -H "accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0", "id":2, "method":"initialized"
  }'
```

### 3. List Available Tools

```bash
curl -s -X POST http://localhost:18000/mcp \
  -H "content-type: application/json" \
  -H "accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0", "id":3, "method":"tools/list"
  }'
```

### 4. Login -> Get Token

```bash
curl -s -X POST http://localhost:18000/mcp \
  -H "content-type: application/json" \
  -H "accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0", "id":4, "method":"tools/call",
    "params": {"name":"auth_login","arguments":{"username":"admin", "password":"admin"}}
  }'
```

### 5. Call Tool Without Authorization (Should Fail)

```bash
curl -s -X POST http://localhost:18000/mcp \
  -H "content-type: application/json" \
  -H "accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0", "id":5, "method":"tools/call",
    "params": {"name":"whoami","arguments":{}}
  }'
```

### 6. Call Tool With Authorization (Replace TOKEN with actual token from login)

```bash
curl -s -X POST http://localhost:18000/mcp \
  -H "content-type: application/json" \
  -H "accept: application/json, text/event-stream" \
  -H "authorization: Bearer TOKEN" \
  -d '{
    "jsonrpc":"2.0", "id":6, "method":"tools/call",
    "params": {"name":"whoami","arguments":{}}
  }'
```