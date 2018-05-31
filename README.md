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
Data processing:
----
    data-producer.py:
    data-stream.py:
    data-storage.py:
    data-redis.py:
Visualization:
----
    main.js:
    
