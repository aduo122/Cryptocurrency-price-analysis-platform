# Cryptocurrency-price-analysis-platform
Introductions
========
    The Cryptocurrency price analysis platform is developed in python and JavaScript. 
    The goal is to monitor the change of Cryptocurrency price. 
    Thanks to https://api.gdax.com, I could get the real time cryptocurrency price.

Pipeline
====
    price data -> kafka -> pyspark -> kafka -> redis -> node.js
                        -> hbase

Usage
====
Docker images:
----
    Zookeeper: confluent/zookeeper
    HBase: harisekhon/hbase
    Kafka: confluent/kafka

Data processing:
----
    data-producer.py: symbol, topic_name, and kafka_broker lcoation are needed.
                  eg. USD-BTC test 127.0.0.1:9092
    data-stream.py: source_topic, target_topic, kafka_broker, batch_duration are needed.
                  eg. test analyzer 127.0.0.1:9092 5
    data-storage.py: topic_name, kafka_broker, data_table, hbase_host are needed.
                  eg. test 127.0.0.1:9092 table1 hbase
    data-redis.py: topic_name, kafka_broker, redis_channel, redis_host, redis_port are needed.
                  eg. analyzer 127.0.0.1:9092 redis 127.0.0.1 8089
Visualization:
----
    main.js: get data from redis, and generate graph by symbol and prices
    ![image](https://user-images.githubusercontent.com/15791192/42296878-7d0f72a6-7fc8-11e8-8822-b74a7400417c.png)

