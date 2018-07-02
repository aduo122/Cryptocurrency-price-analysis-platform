#python3
import argparse
import atexit
import happybase
import logging
from kafka import KafkaConsumer
import json
from kafka.errors import KafkaError


logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG)

# Default parameters
topic_name = 'analyzer'
kafka_broker = '127.0.0.1:9092'
data_table = 'cryptocurrency'
hbase_host = 'myhbase'


def persist_data(data, hbase_connection, data_table):
    """
    :param data:  Price data to store
    :param hbase_connection: Hbae to use
    :param data_table: Table to store data
    :return:
    """
    try:
        logger.debug('Start to persist data to hbase %s', data)
        parsed = json.loads(data)
        symbol = parsed.get('Symbol')
        price = float(parsed.get('LastTradePrice'))
        timestamp = parsed.get('Timestamp')

        table = hbase_connection.table(data_table)
        row_key = "%s-%s" % (symbol, timestamp)
        logger.info('Storing values with row key %s' % row_key)
        table.put(row_key, {'family:symbol': str(symbol),
                            'family:timestamp': str(timestamp),
                            'family:price': str(price)})
        logger.info('Persisted data to hbase for symbol: %s, price:%f, timestamp: %s',
                    symbol, price, timestamp)
    except Exception as e:
        logger.error('Failed to persist to hbase for %s', str(e))


def shutdown_hook(consumer, hbase_connection):
    try:
        logger.info('Closing Kafka consumer')
        consumer.close()
        logger.info('Kafka consumer closed')
        logger.info('Closing Hbase connection')
        hbase_connection.close()
        logger.info('Hbase connection closed')
    except Exception as e:
        logger.warn('Failed to close consumer/connection, caused by: %s', str(e))
    finally:
        logger.info('Exiting program')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('topic_name', help='the kafka topic to pull from')
    parser.add_argument('kafka_broker', help='the location of the kafkabroker')
    parser.add_argument('data_table', help='the data table to use')
    parser.add_argument('hbase_host', help='the host name of hbase')

    #parse args
    args = parser.parse_args()
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker
    data_table = args.data_table
    hbase_host = args.hbase_host

    #initial Kafka consumer
    consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_broker)

    #initial Hbase connection
    hbase_connection = happybase.Connection(hbase_host)

    # Create table is not exists
    logger.debug(str(data_table))
    for table in hbase_connection.tables():
        logger.debug('Current Tables : ' + str(table))
    if str.encode(data_table) not in hbase_connection.tables():
        # Create data_table
        # {Symbol:symbol, LastTradePrice:lasttradeprice, Timestamp:timestamp}
        # Symbol_Timestamp as key, LastTradePrice as value
        hbase_connection.create_table(data_table, {'family' : dict()})

    # Setup proper shutdown hook
    atexit.register(shutdown_hook, consumer, hbase_connection)

    for msg in consumer:
        persist_data(msg.value, hbase_connection, data_table)
