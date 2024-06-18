FROM python:3.9-alpine

WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN apk add --no-cache --virtual .build-deps \
        gcc musl-dev libffi-dev openssl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Copy the rest of the application code
COPY . /app

# Set environment variables
ENV SEVERITY=all
ENV PROJECT_ID=gck-keda
ENV SUBSCRIPTION_LOG_NAME=direct_logs
ENV SUBSCRIPTION_TOPIC_NAME=topic_logs

CMD ["python", "gg-consumer.py"]
