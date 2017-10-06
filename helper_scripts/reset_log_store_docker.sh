#!/usr/bin/env bash

# Paths to Kafka and Flink (docker setup).
# Please adapt according to your configuration.
FLINK_PATH=/opt/flink
KAFKA_PATH=/opt/kafka

printf 'Emptying Kafka topics.'
for topic in 'marketSituation' 'cumulativeRevenueBasedMarketshare' 'updateOffer' 'cumulativeRevenueBasedMarketshareHourly' 'cumulativeRevenueBasedMarketshareDaily' 'cumulativeTurnoverBasedMarketshare' 'cumulativeTurnoverBasedMarketshareHourly' 'cumulativeTurnoverBasedMarketshareDaily' 'cumulativeAmountBasedMarketshare' 'cumulativeAmountBasedMarketshareHourly' 'cumulativeAmountBasedMarketshareDaily' 'revenue' 'buyOffer' 'producer' 'revenuePerMinute' 'profitPerMinute' 'revenuePerHour' 'profitPerHour'
do
  docker exec masterprojectpricewars_kafka_1 ${KAFKA_PATH}/bin/kafka-topics.sh --delete --zookeeper zookeeper:2181 --topic $topic > /dev/null
  printf '.'
done

printf '\nRemoving old CSV files and restarting reverse-kafka-proxy to empty its cache.'
docker exec masterprojectpricewars_kafka-reverse-proxy_1 find /loggerapp/data/ -name '*.csv' -exec rm -f {} \;
docker restart masterprojectpricewars_kafka-reverse-proxy_1

printf '\nCanceling flink jobs.'
docker exec masterprojectpricewars_flink-jobmanager_1 ${FLINK_PATH}/bin/flink list -r | awk '{split($0, a, " : "); print a[2]}' | while read line; do
    [ -z "$line" ] && continue
    docker exec masterprojectpricewars_flink-jobmanager_1 ${FLINK_PATH}/bin/flink cancel $line > /dev/null
    printf '.'
done

printf '\nRestarting flink jobs.'
for file in `docker exec masterprojectpricewars_flink-jobmanager_1 ls /analytics/ | grep jar`
do
    if [ "${file}" != "${file%.jar}" ];then
        docker exec masterprojectpricewars_flink-jobmanager_1 ${FLINK_PATH}/bin/flink run -d /analytics/$file > /dev/null
    fi
    printf '.'
done

echo ''
