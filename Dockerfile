FROM python:3.13-slim

WORKDIR /app

COPY api/tinycloud/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["flask", "run", "--host=0.0.0.0", "--port=8081", "--debug"]