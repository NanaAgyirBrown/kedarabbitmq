import pika
import logging


def consumer_log():
    try:
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='logs', queue=queue_name)
        logging.info(' [*] Waiting for logs. To exit press Ctrl+C')

        def callback(ch, method, properties, body):
            logging.info(f' [*] Received - {body.decode()}')

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

