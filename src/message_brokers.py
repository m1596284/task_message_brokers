import pika
import os
from time import sleep


def on_channel_closed():
    print('Channel was closed, reconnecting...', flush=True)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_name))
    channel = connection.channel()
    channel.queue_declare(queue='test_queue')
    channel.queue_purge(queue='test_queue')


def send_message():
    message = "Hello, World!"
    channel.basic_publish(exchange='', routing_key='test_queue', body=message)


def receive_message():
    def callback(channel, method, properties, body):
        print(f"Received message: {body}", flush=True)

    channel.basic_consume(queue='test_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages...', flush=True)
    channel.start_consuming()


if __name__ == '__main__':
    # Wait for RabbitMQ to start
    print('Waiting 10s for RabbitMQ to start...', flush=True)
    sleep(10)

    # Setup connection, channel and queue
    host_name = os.getenv('RABBITMQ_HOST', 'localhost')
    print(f'Connecting to RabbitMQ on {host_name}...', flush=True)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_name))
    channel = connection.channel()
    channel.add_on_cancel_callback(on_channel_closed)
    channel.queue_declare(queue='test_queue')
    channel.queue_purge(queue='test_queue')

    # Send message to queue
    send_message()

    # Receive message from queue
    receive_message()
