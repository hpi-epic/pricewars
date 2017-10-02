#!/usr/bin/env bash

printf 'Starting consumer: '
SETTINGS=`curl -s -X GET -H "Content-Type: application/json" http://consumer:3000/setting`
SUCC=`echo $SETTINGS | grep -c 'consumer_per_minute'`

if [ "$SUCC" = "1" ]
then
  RET=`curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$SETTINGS" http://consumer:3000/setting`
  if [ "$RET" = "200" ]
  then
    echo 'successful.'
  fi
else
  echo 'unsuccessful (error: could not get settings before starting.) Exiting.'
fi

