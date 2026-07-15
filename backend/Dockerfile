FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/models/huggingface \
    HF_HUB_DISABLE_XET=1

COPY requirements-docker.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch==2.6.0 \
      --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements-docker.txt

COPY webapp ./webapp

EXPOSE 8000

CMD ["python", "webapp/sentiment-api-basic.py"]
