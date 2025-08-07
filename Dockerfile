FROM python:3.13-slim

WORKDIR /app

COPY api/tinycloud/requirements.txt .

RUN pip install -r requirements.txt

COPY api/tinycloud/ .

EXPOSE 5000

CMD ["python", "app.py"]