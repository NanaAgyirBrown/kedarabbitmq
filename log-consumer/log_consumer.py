import sys
import os
import pika
import logging


def consumer_log():
    try:
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
        channel = connection.channel()

        # This consumes FANOUT logs
        # channel.exchange_declare(exchange='logs', exchange_type='fanout')

        # We want to consume logs based on SEVERITY - info, warning or error
        channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Get severities from environment variable
        severities = os.getenv('SEVERITY', 'info').split(',')

        for severity in severities:
            if severity in ['info', 'warning', 'error']:
                channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

        print(' [*] Waiting for logs. To exit press Ctrl+C')

        def callback(ch, method, properties, body):
            print(f' [*] {method.routing_key}: {body.decode()}')

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Connection error: {e}")
    except pika.exceptions.ChannelError as e:
        logging.error(f"Channel error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()
            logging.info("Connection closed")


if __name__ == '__main__':
    consumer_log()

