FROM python:3.9-alpine

WORKDIR /app

COPY . /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV SEVERITY all

CMD ["python", "log_consumer.py"]