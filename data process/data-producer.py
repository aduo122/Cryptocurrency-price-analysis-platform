# python3
import argparse
import logging
import schedule
import atexit
import time
import json

import requests

from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG)

API_BASE = 'https://api.gdax.com'

def check_symbol(symbol):
    """
    helper method check if symbol exist in coinbase API
    """
    logger.debug('Checking symbol.')
    try:
        # get apibase products id, BTC - USD or BTC - EUR
        response = requests.get(API_BASE + '/products')
        product_ids = [product['id'] for product in response.json()]

        if symbol not in product_ids:
            logger.warn("symbol %s not supported. The list of supported symbol: %s", symbol, product_ids)
            exit()
    except Exception as e:
        logger.warn('Fail to fetch products')

# Core Function, get price data
def fetch_price(symbol, producer, topic_name):
    """
    :param symbol:
    :param producer:
    :return: None
    retrieve data and send to kafka
    """
    logger.debug('Start to fetch price for %s', symbol)
    try:
        response = requests.get('%s/products/%s/ticker' % (API_BASE, symbol))
        price = response.json()['price']

        timestamp = time.time()
        payload = {'Symbol': str(symbol),
                   'LastTradePrice': str(price),
                   'Timestamp': str(timestamp)}
        logger.debug('Retrieved %s info %s', symbol, payload)

        # value needs to be bytes for python3
        producer.send(topic=topic_name, value=json.dumps(payload).encode('utf8'), timestamp_ms=int(time.time() * 1000))

        logger.debug('Sent price for %s to Kafka' % symbol)
    except KafkaTimeoutError as timeout_e:
        logger.warning('Failed to send messages to kafka, caused by: %s', str(timeout_e))
    except Exception as e:
        logger.warning('Failed to fetch price: %s', (e))



def shutdown_hook(producer):
    try:
        producer.flush(10)
    except KafkaError as kafka_e:
        logger.warn('Failed to flush pending messages to kafka, caused by: %s', str(kafka_e))
    finally:
        try:
            producer.close(10)
        except Exception as e:
            logger.error('Failed to close kafka connection, caused by %s', str(e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol', help='the symbol you want to pull')
    parser.add_argument('topic_name', help='the kafka topic push to')
    parser.add_argument('kafka_broker', help='the location of the kafka broker')

    # Parse arguments
    args = parser.parse_args()
    symbol = args.symbol
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker

    # Check the symbol is supported
    check_symbol(symbol)

    # Kafka start!
    # start KafkaProducer
    producer = KafkaProducer(bootstrap_servers=kafka_broker)

    # use schedule to get data continuously and save to kafka OR could use while loop
    schedule.every(1).second.do(fetch_price, symbol, producer, topic_name)

    # end KafkaProducer
    atexit.register(shutdown_hook, producer)

    while True:
        schedule.run_pending()
        time.sleep(1)

