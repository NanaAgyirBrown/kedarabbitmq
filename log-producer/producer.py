import datetime
import os
import random

import pika
import sys

project_id = "gck-keda"

def produce_logs(counter):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    # severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    # We want to randomly generate severity
    severities = ['info', 'warning', 'error']
    severity = random.choice(severities)

    message = ' '.join(sys.argv[2:]) or f"{counter} : This is emitted from the producer @ {datetime.datetime.now()}"
    channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)

    print(f" [x] Sent {severity} : {message}")
    connection.close()


def produce_topics(counter):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
    routing_keys = os.environ['ROUTING_KEYS'].split(',')

    key = random.choice(routing_keys)
    routing_key = key if len(key.split('.')) > 1 else 'anonymous.info'

    message = ' '.join(sys.argv[2:]) or f'{counter} : This is a topic emission for {routing_key}'

    channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)

    print(f" [x] broadcasted : {message}")
    connection.close()


if __name__ == '__main__':
    counter = 0
    while True:
        counter += 1
        produce_logs(counter)
        produce_topics(counter)
