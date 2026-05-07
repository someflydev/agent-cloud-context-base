FROM python:3.12-slim
WORKDIR /app
COPY src/job/ ./
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
