FROM python:3.12.7-slim

# Install system dependencies including tesseract-ocr with exact versions
RUN apt-get update && apt-get install -y \
    tesseract-ocr=4.1.1-2.1build1 \
    tesseract-ocr-eng=1:4.00~git30-7274cfa-1.1 \
    libgl1-mesa-glx=22.0.5-0ubuntu0.3 \
    libglib2.0-0=2.72.4-0ubuntu2.3 \
    libsm6=2:1.2.3-1build2 \
    libxext6=2:1.3.4-1build1 \
    libxrender-dev=1:0.9.10-1build4 \
    libgomp1=12.3.0-1ubuntu1~22.04 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory with full path
WORKDIR /app

# Install Poetry with exact version
RUN /usr/local/bin/pip install poetry==1.8.4

# Copy poetry files with full paths
COPY ./pyproject.toml ./poetry.lock /app/

# Configure poetry and install dependencies with full paths
RUN /usr/local/bin/poetry config virtualenvs.create false \
    && /usr/local/bin/poetry install --no-dev --no-interaction --no-ansi

# Copy application code with full paths
COPY . /app/

# Expose port
EXPOSE 8000

# Run the application with full paths
CMD ["/usr/local/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
