import pika
import sys
import json
# Use the IP address of your RabbitMQ server
rabbitmq_ip = '65.109.207.204'

print("Connecting to RabbitMQ...")
credentials = pika.PlainCredentials('user', 'password')
parameters = pika.ConnectionParameters(rabbitmq_ip, 5672, '/', credentials)

try:
    connection = pika.BlockingConnection(parameters)
    print("Connected to RabbitMQ")

    channel = connection.channel()
    channel.queue_declare(queue='test_queue')
    print("Queue declared")

    # Publish a single message
    channel.basic_publish(exchange='', routing_key='test_queue', body=json.dumps({"message": "Hello World"}))
    print(" [x] Sent 'Hello, World!'")

except pika.exceptions.AMQPConnectionError as e:
    print(f"Connection error: {e}")
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()
        print("Connection closed")

sys.exit(0)

