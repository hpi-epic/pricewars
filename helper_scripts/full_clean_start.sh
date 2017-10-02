#!/bin/bash
# This file is intended to be used in case of severe docker problems. It stops
# and removes all docker containers, then fully removes the docker images
# (leading to a time consuming rebuild), followed by a docker-compose up.
# (thanks to @carlambroselli).
rm -rf docker-mounts/*

docker stop masterprojectpricewars_management-ui_1
docker stop masterprojectpricewars_merchant-simple-competition-logic1_1
docker stop masterprojectpricewars_merchant-machine-learning_1
docker stop masterprojectpricewars_merchant-sample-fix-price_1
docker stop masterprojectpricewars_merchant-sample-second-cheapest_1
docker stop masterprojectpricewars_merchant-sample-cheapest_1
docker stop masterprojectpricewars_merchant-sample-random-third_1
docker stop masterprojectpricewars_merchant-simple-competition-logic2_1
docker stop masterprojectpricewars_merchant-sample-two-bound_1
docker stop masterprojectpricewars_consumer_1
docker stop masterprojectpricewars_marketplace_1
docker stop masterprojectpricewars_flink-taskmanager_1
docker stop masterprojectpricewars_kafka-reverse-proxy_1
docker stop masterprojectpricewars_flink-jobmanager_1
docker stop masterprojectpricewars_producer_1
docker stop masterprojectpricewars_kafka_1
docker stop masterprojectpricewars_postgres_1
docker stop masterprojectpricewars_zookeeper_1
docker stop masterprojectpricewars_redis_1
docker stop masterprojectpricewars_analytics_1

docker-compose down

docker rm masterprojectpricewars_management-ui_1
docker rm masterprojectpricewars_merchant-simple-competition-logic1_1
docker rm masterprojectpricewars_merchant-machine-learning_1
docker rm masterprojectpricewars_merchant-sample-fix-price_1
docker rm masterprojectpricewars_merchant-sample-second-cheapest_1
docker rm masterprojectpricewars_merchant-sample-cheapest_1
docker rm masterprojectpricewars_merchant-sample-random-third_1
docker rm masterprojectpricewars_merchant-simple-competition-logic2_1
docker rm masterprojectpricewars_merchant-sample-two-bound_1
docker rm masterprojectpricewars_consumer_1
docker rm masterprojectpricewars_marketplace_1
docker rm masterprojectpricewars_flink-taskmanager_1
docker rm masterprojectpricewars_kafka-reverse-proxy_1
docker rm masterprojectpricewars_flink-jobmanager_1
docker rm masterprojectpricewars_producer_1
docker rm masterprojectpricewars_kafka_1
docker rm masterprojectpricewars_postgres_1
docker rm masterprojectpricewars_zookeeper_1
docker rm masterprojectpricewars_redis_1
docker rm masterprojectpricewars_analytics_1

docker rmi pricewars/management-ui
docker rmi pricewars/merchant
docker rmi pricewars/merchant
docker rmi pricewars/merchant
docker rmi pricewars/merchant
docker rmi pricewars/merchant
docker rmi pricewars/merchant
docker rmi pricewars/merchant
docker rmi pricewars/merchant
docker rmi pricewars/consumer
docker rmi pricewars/marketplace
docker rmi pricewars/kafka-reverse-proxy
docker rmi pricewars/producer
docker rmi pricewars/analytics

docker-compose up
