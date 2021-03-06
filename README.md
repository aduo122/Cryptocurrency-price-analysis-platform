# Cryptocurrency-price-analysis-platform
Introductions
========
    The Cryptocurrency price analysis platform is developed in python and JavaScript. 
    The goal is to monitor the change of Cryptocurrency price. 
    Thanks https://api.gdax.com for providing the real time cryptocurrency price.

Pipeline
====
    Price Data (Web API) -> Kafka -> Pyspark -> Kafka -> Redis -> Node.js
                         -> Hbase

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
                  eg. test analyzer 127.0.0.1:9092 300
    data-storage.py: topic_name, kafka_broker, data_table, hbase_host are needed.
                  eg. test 127.0.0.1:9092 table1 hbase
    data-redis.py: topic_name, kafka_broker, redis_channel, redis_host, redis_port are needed.
                  eg. analyzer 127.0.0.1:9092 redis 127.0.0.1 8089
Visualization:
----
    main.js: get data from redis, and generate graph by symbol and prices
![image](https://github.com/aduo122/Cryptocurrency-price-analysis-platform/blob/master/candlestick_graph.png)

