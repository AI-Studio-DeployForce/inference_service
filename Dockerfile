# inference_service/Dockerfile
FROM python:3.9-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git \
        libgl1   libglib2.0-0  && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. copy the .env file first
COPY .env .

# 3. copy the clearml.conf to the correct location
COPY clearml.conf /root/clearml.conf

# 4. copy the rest of the source code
COPY . .

# 5. Download the model weights during build
RUN python utils/download_weights.py

# Ports & env
ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8001 \
    PYTHONUNBUFFERED=1
EXPOSE 8001
CMD ["flask", "run"]