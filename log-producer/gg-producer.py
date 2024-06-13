import datetime
import os
import random
import sys
from google.cloud import pubsub_v1

project_id = "gck-keda"

publisher = pubsub_v1.PublisherClient()
topic_log_name = "direct_logs"  # The Pub/Sub topic for direct logs
topic_log_path = publisher.topic_path(project_id, topic_log_name)

topic_topic_name = "topic_logs"  # The Pub/Sub topic for topic logs
topic_topic_path = publisher.topic_path(project_id, topic_topic_name)

def produce_logs(counter):
    severities = ['info', 'warning', 'error']
    severity = random.choice(severities)

    message = ' '.join(sys.argv[2:]) or f"{counter} : This is emitted from the producer @ {datetime.datetime.now()}"
    data = message.encode("utf-8")
    future = publisher.publish(topic_log_path, data, severity=severity)
    print(f" [x] Sent {severity} : {message}")
    future.result()

def produce_topics(counter):
    routing_keys = os.environ.get('ROUTING_KEYS', 'anonymous.info').split(',')

    key = random.choice(routing_keys)
    routing_key = key if len(key.split('.')) > 1 else 'anonymous.info'

    message = ' '.join(sys.argv[2:]) or f'{counter} : This is a topic emission for {routing_key}'
    data = message.encode("utf-8")
    future = publisher.publish(topic_topic_path, data, routing_key=routing_key)
    print(f" [x] broadcasted : {message}")
    future.result()

if __name__ == '__main__':
    counter = 0
    while True:
        counter += 1
        produce_logs(counter)
        produce_topics(counter)
