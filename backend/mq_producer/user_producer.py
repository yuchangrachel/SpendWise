import pika

def send_to_rabbitmq(exchange, queue_name, message, routing_key):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
        channel = connection.channel()

        # declare exchange (ensure it exists)
        channel.exchange_declare(exchange=exchange, exchange_type="direct", durable=True)

        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)

        # publish the message
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
        )
        print(f"Message sent to RabbitMQ: {message}")
    except Exception as e:
        print(f"Failed to send message to RabbitMQ: {e}")
    finally:
        if 'connection' in locals():
            connection.close()