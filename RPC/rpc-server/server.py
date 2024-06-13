import pika


def server_start():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue', durable=True)

    def fin(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fin(n - 1) + fin(n - 2)

    def on_request(ch, method, props, body):
        n = int(body)

        print(f" [.] fib({n})")
        response = fin(n)
        ch.basic_publish(exchange='', routing_key=props.reply_to,
                         properties=pika.BasicProperties(correction_id = props.correction_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    print(' [*] Awaiting RPC requests')
    channel.start_consuming()

