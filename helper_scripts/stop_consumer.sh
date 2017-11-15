#!/usr/bin/env bash


printf 'Stopping consumer: '
RET=`curl -s -o /dev/null -w "%{http_code}" -X DELETE -H "Content-Type: application/json" http://consumer:3000/setting`

if [ "$RET" = "200" ]
then
  echo 'successful.'
else
  echo 'unsuccessful.'
fi

