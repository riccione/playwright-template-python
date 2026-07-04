FROM mcr.microsoft.com/playwright:v1.52.0-noble

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

COPY . .

RUN uv run playwright install --with-deps

ENV CI=true

CMD ["uv", "run", "pytest"]
