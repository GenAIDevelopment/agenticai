FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY server.py ./
ENV MCP_HOST="0.0.0.0"

EXPOSE 8000

CMD ["uv", "run", "python", "server.py"]