import pika
import time

def callback(ch, method, properties, body):
    print(f"Received {body}")

def main():
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)

    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='test_queue')
            channel.basic_consume(queue='test_queue', on_message_callback=callback, auto_ack=True)
            print('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("Couldn't connect to RabbitMQ. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    main()
