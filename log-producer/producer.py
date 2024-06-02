import datetime
import random

import pika
import sys


def produce_logs(counter):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
    channel = connection.channel()

    # In this snippet we are publishing our logs to as FANOUT
    # channel.exchange_declare(exchange='logs', exchange_type='fanout')
    # message = ' '.join(sys.argv[1:]) or f"info: This is emitted from the producer @ {datetime.datetime.now()}"
    # channel.basic_publish(exchange='logs', routing_key='', body=message)

    # In this snippet we will publish using Direct Exchange and Routing keys
    # This allows the Consumer to consumer what it requires
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    # severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    # We want to randomly generate severity
    severities = ['info', 'warning', 'error']
    severity = random.choice(severities)

    message = ' '.join(sys.argv[2:]) or f"{counter} : This is emitted from the producer @ {datetime.datetime.now()}"
    channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)

    print(f" [x] Sent {severity} : {message}")
    connection.close()


if __name__ == '__main__':
    counter = 0
    while True:
        counter += 1
        produce_logs(counter)
