FROM python:3.11-slim
WORKDIR /app
COPY ai_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ai_service/ .
COPY backoffice/models/ ./backoffice/models/
COPY backoffice/__init__.py ./backoffice/__init__.py
COPY inventory.db .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]