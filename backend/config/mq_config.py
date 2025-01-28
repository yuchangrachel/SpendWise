import pika

DEFAULT_CREDENTIALS = pika.PlainCredentials('guest', 'guest')

def get_rabbitmq_connect():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host="127.0.0.1", # change when production
            port=5672,
            virtual_host="/",
            credentials=DEFAULT_CREDENTIALS
        )
    )