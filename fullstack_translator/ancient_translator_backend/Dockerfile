FROM python:3.12.7-slim

# Install system dependencies including tesseract-ocr with additional debugging
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    which \
    && rm -rf /var/lib/apt/lists/*

# Verify tesseract installation with comprehensive PATH setup
RUN which tesseract && \
    tesseract --version && \
    ln -sf /usr/bin/tesseract /usr/local/bin/tesseract && \
    echo "export PATH=/usr/bin:/usr/local/bin:$PATH" >> /etc/environment

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
