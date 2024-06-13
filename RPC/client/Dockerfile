FROM python:3.9-alpine
LABEL authors="Nana Brown"

WORKDIR /app
COPY . /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "client.py"]