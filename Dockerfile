FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


# Copy the source code into the container
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.infra.server.main:app", "--host", "0.0.0.0", "--port", "8000"]