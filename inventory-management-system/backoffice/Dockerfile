FROM python:3.11-slim
WORKDIR /app
COPY backoffice/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backoffice/ ./backoffice/
COPY inventory.db .
EXPOSE 5000
ENV PYTHONPATH=/app
CMD ["python", "-m", "flask", "--app", "backoffice.app", "run", "--host", "0.0.0.0", "--port", "5000"]