import pika


def on_channel_closed():
    print('Channel was closed, reconnecting...')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='test_queue')
    channel.queue_purge(queue='test_queue')


def send_message():
    message = "Hello, World!"
    channel.basic_publish(exchange='', routing_key='test_queue', body=message)


if __name__ == '__main__':
    # Setup connection, channel and queue
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.add_on_cancel_callback(on_channel_closed)
    channel.queue_declare(queue='test_queue')
    channel.queue_purge(queue='test_queue')

    # Send message to queue
    send_message()
