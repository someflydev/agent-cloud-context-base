FROM python:3.12-slim
WORKDIR /app
COPY src/api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/api/ ./
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
