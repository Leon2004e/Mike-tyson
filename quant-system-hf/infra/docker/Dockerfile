FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -e .
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
