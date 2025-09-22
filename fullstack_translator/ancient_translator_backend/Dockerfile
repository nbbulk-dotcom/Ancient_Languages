# Builder stage for tesseract and assets
FROM debian:stable-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr tesseract-ocr-eng libtesseract-dev pkg-config ca-certificates \
    poppler-utils wget unzip \
 && rm -rf /var/lib/apt/lists/*

# Final app image
FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
# ensure /usr/bin is explicit in PATH
ENV PATH="/usr/bin:${PATH}"

# copy tesseract binaries and tessdata
COPY --from=builder /usr/bin/tesseract /usr/bin/tesseract
COPY --from=builder /usr/share/tesseract-ocr /usr/share/tesseract-ocr
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy app
COPY app /app/app

# expose and healthcheck
EXPOSE 8000
COPY Dockerfile.healthcheck /healthcheck.sh
RUN chmod +x /healthcheck.sh
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD /healthcheck.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
