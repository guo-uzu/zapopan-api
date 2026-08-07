FROM python:3.14
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /code
COPY pyproject.toml uv.lock* /code/
RUN uv pip install --system --no-cache -r pyproject.toml
COPY ./app /code/app
EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
