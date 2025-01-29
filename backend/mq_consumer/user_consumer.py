import pika
import os
import logging

LOG_DIR = "../logs"
LOG_FILE = os.path.join(LOG_DIR, "consume.log")
EXCHANGE = 'activity_logs_exchange'
QUEUE_NAME = 'user_register_queue'
ROUTING_KEY = 'register'

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        # logging.StreamHandler()   print on console
    ]
)

def start_consumer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
        channel = connection.channel()

        # declare exchange and queue, and bind them
        channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct", durable=True)
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.queue_bind(exchange=EXCHANGE, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

        # print("Waiting for messages. To exit press CTRL+C")

        def callback(ch, method, properties, body):
            try:
                logging.info(f"Received: {body.decode('utf-8')}") # decode base64-encoded string 
            except Exception as e:
                logging.error(f"Error decoding message: {e}")

        # consume messages ack=True, make sure consumer receive message from producer
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info("\nConsumer stopped.")
    except Exception as e:
        logging.error(f"Error in consumer: {e}")
    finally:
        if 'connection' in locals():
            connection.close()


if __name__ == '__main__':
    start_consumer()
