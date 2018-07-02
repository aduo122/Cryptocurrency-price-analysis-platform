#python3
import argparse
import atexit
import time

import happybase
import logging

from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from kafka.errors import KafkaError, KafkaTimeoutError
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data-stream')
logger.setLevel(logging.DEBUG)

# topic_name = 'analyzer'
# kafka_broker = '127.0.0.1:9092'
# data_table = 'cryptocur'
#
# hbase_host = 'myhbase'

def shutdown_hook(producer):
    try:
        producer.flush(10)
    except KafkaError as kafka_e:
        logger.warn('Failed to flush pending messages to kafka, caused by: %s', str(kafka_e))
    finally:
        try:
            producer.close(10)
        except Exception as e:
            logger.warn('Failed to close kafka connection, caused by %s', str(e))

def process_stream(stream, kafka_producer, target_topic):
    def pair(data):
        record = json.loads(data.encode('utf-8'))
        return record.get('Symbol'),(float(record.get('LastTradePrice')), 1, float(record.get('LastTradePrice')), float(record.get('LastTradePrice')), float(record.get('LastTradePrice')))

    def send_to_kafka(rdd):
        results = rdd.collect()
        for r in results:
            data = json.dumps(
                {
                    'Symbol':r[0],
                    'Timestamp':time.time(),
                    'Average':r[1],
                    'Max':r[2],
                    'Min':r[3],
                    'Start_price':r[4],
                    'End_price':r[5]
                }).encode('utf-8')
            try:
                logger.info('Sending average price %s to kafka', data)
                kafka_producer.send(target_topic, value=data)
            except KafkaError as error:
                logger.warn('Something wrong')

    stream.map(pair).reduceByKey(lambda a,b:(a[0] + b[0], a[1] + b[1], max(a[2], b[2]), min(a[3], b[3]), a[4], b[4])).map(lambda k:(k[0], k[1][0]/k[1][1], k[1][2], k[1][3], k[1][4], k[1][5])).foreachRDD(send_to_kafka)





if __name__ == '__main__':
    # Setup command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('source_topic',help='kafka topic to subscribe from')
    parser.add_argument('target_topic', help='kafka topic to send')
    parser.add_argument('kafka_broker', help='kafka broker')
    parser.add_argument('batch_duration', help='batch duration')

    args = parser.parse_args()
    source_topic = args.source_topic
    target_topic = args.target_topic
    kafka_broker = args.kafka_broker
    batch_duration = int(args.batch_duration)

    sc = SparkContext('local[2]','AveragePrice')
    sc.setLogLevel('INFO')
    ssc = StreamingContext(sc,batch_duration)

    directKafkaStream = KafkaUtils.createDirectStream(ssc, [source_topic], {'metadata.broker.list':kafka_broker})

    stream = directKafkaStream.map(lambda x:x[1])

    kafka_producer = KafkaProducer(bootstrap_servers=kafka_broker)

    process_stream(stream, kafka_producer, target_topic)

    atexit.register(shutdown_hook, kafka_producer)

    ssc.start()
    ssc.awaitTermination()
