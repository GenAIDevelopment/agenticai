# Human-in-the-Loop Local Model

## Running the Application

Start the server with:

```bash
uv run uvicorn main:app --reload --port 8000
```

## API Endpoints

### Start a new conversation

```bash
curl -s -X POST "http://localhost:8000/runs" \
  -H "content-type: application/json" \
  -d '{"user_text":"What is the capital of India?"}'
```

### Approve a response

```bash
curl -s -X POST "http://localhost:8000/runs/<THREAD_ID>/resume" \
  -H "content-type: application/json" \
  -d '{"approved": true, "reviewer_id":"khaja"}'
```

### Reject a response with feedback

```bash
curl -s -X POST "http://localhost:8000/runs/<THREAD_ID>/resume" \
  -H "content-type: application/json" \
  -d '{"approved": false, "notes":"Answer must be one word only", "reviewer_id":"khaja"}'
```
