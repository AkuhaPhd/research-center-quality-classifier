# Use slim Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project metadata and Astral UV binaries
COPY pyproject.toml uv.lock README.md ./
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Sync dependencies with uv
RUN uv sync --frozen

# Copy all app code
COPY . .

# Export dependencies to pip and install globally
RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]