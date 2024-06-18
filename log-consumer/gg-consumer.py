import os
import logging
from google.cloud import pubsub_v1

project_id = os.getenv('PROJECT_ID')
subscription_log_name = os.getenv('SUBSCRIPTION_LOG_NAME')
subscription_topic_name = os.getenv('SUBSCRIPTION_TOPIC_NAME')


def consumer_log():
    subscriber = pubsub_v1.SubscriberClient()

    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def callback_log(message):
        print(f" [*] {message.attributes['severity']}: {message.data.decode('utf-8')}")
        message.ack()

    def callback_topic(message):
        print(f" [x] {message.attributes['routing_key']}: {message.data.decode('utf-8')}")
        message.ack()

    if os.getenv('TYPE') == 'Routing':
        subscription_path_log = subscriber.subscription_path(project_id, subscription_log_name + "-sub")
        try:
            print(' [*] Waiting for logs. To exit press Ctrl+C')
            print(f'subscription_path_log - {subscription_path_log}')
            streaming_pull_future_log = subscriber.subscribe(subscription_path_log, callback=callback_log)
            streaming_pull_future_log.result()
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        finally:
            streaming_pull_future_log.cancel()
    elif os.getenv('TYPE') == 'Topics':
        subscription_path_topic = subscriber.subscription_path(project_id, subscription_topic_name + "-sub")
        try:
            print(' [*] Waiting for logs. To exit press Ctrl+C')
            print(f'subscription_path_topic - {subscription_path_topic}')
            streaming_pull_future_topic = subscriber.subscribe(subscription_path_topic, callback=callback_topic)
            streaming_pull_future_topic.result()
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        finally:
            streaming_pull_future_topic.cancel()


if __name__ == '__main__':
    consumer_log()
