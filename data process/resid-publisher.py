#python3
import argparse
import atexit
import logging
import redis

from kafka import KafkaConsumer
from kafka.errors import KafkaError


logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('redis-publisher')
logger.setLevel(logging.DEBUG)

def shutdown_hook(consumer):
    logger.info('Shut down Kafka consumer')
    try:
        consumer.close()
    except Exception as e:
        logger.warn('Something Wrong s%', str(e))

if __name__ == '__main__':
    # Setup command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('topic_name', help='the kafka topic to pull from')
    parser.add_argument('kafka_broker', help='the location of the kafkabroker')
    parser.add_argument('redis_channel', help='the redis channel to publish to')
    parser.add_argument('redis_host', help='the host of redis server')
    parser.add_argument('redis_port', help='the port of redis server')

    # Parse arguments
    args = parser.parse_args()
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker
    redis_channel = args.redis_channel
    redis_host = args.redis_host
    redis_port = args.redis_port

    # Instantiate kafka consumer
    kafka_consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_broker)

    # Instantiate redis client
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

    # End KafkaConsumer
    atexit.register(shutdown_hook, kafka_consumer)

    for msg in kafka_consumer:
        logger.info('Received new data from kafka %s', str(msg))
        redis_client.publish(redis_channel, str(msg))