FROM python:3.12-slim
WORKDIR /app
COPY src/cronjob/ ./
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
