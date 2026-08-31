FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango1.0-dev \
    libcairo2-dev \
    pkg-config \
    libglib2.0-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    tesseract-ocr \
    tesseract-ocr-fra \
    tesseract-ocr-eng \
    libpango-1.0-0 \
    libcairo2 \
    libglib2.0-0 \
    libharfbuzz0b \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

WORKDIR /app
COPY . .

ENTRYPOINT ["python", "run.py"]
CMD ["--help"]
