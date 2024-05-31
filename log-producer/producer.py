import datetime
import pika
import sys


def produce_logs(counter):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    message = ' '.join(sys.argv[1:]) or f"info: This is emitted from the producer @ {datetime.datetime.now()}"
    channel.basic_publish(exchange='logs', routing_key='', body=message)

    print(f"{counter} Sent %r" % message)
    connection.close()


if __name__ == '__main__':
    counter = 0
    while True:
        counter += 1
        produce_logs(counter)