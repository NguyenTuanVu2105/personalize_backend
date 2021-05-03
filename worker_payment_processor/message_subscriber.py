import logging

import pika

from HUB import settings

logger = logging.getLogger(__name__)
parameters = pika.URLParameters(settings.BROKER_URL)


def init_channel(channel, queue_name, exchange_name):
    channel.exchange_declare(exchange=exchange_name, durable=True)
    channel.queue_declare(queue=queue_name, auto_delete=False, durable=True)
    channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key="default")


def subscribe(queue_name, message_handler):
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    try:
        init_channel(channel, queue_name, queue_name)
        channel.basic_consume(queue=queue_name, consumer_callback=message_handler)
        channel.start_consuming()
    except Exception as e:
        logger.exception(e)
        channel.stop_consuming()
        connection.close()
