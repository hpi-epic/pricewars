#!/usr/bin/env bash

echo 'Please be aware that this script currently does not ensure the probabilities add up to 100%.'
echo 'Default to: 50% logit behaviour, 30% cheapest behaviour, and 20% random behaviour.'

if [ -z "$PERCENTAGE_LOGIT" ]; then
    PERCENTAGE_LOGIT=50
fi

if [ -z "$PERCENTAGE_CHEAPEST" ]; then
    PERCENTAGE_CHEAPEST=30
fi

if [ -z "$PERCENTAGE_SEC_CHEAPEST" ]; then
    PERCENTAGE_SEC_CHEAPEST=10
fi

if [ -z "$PERCENTAGE_RANDOM" ]; then
    PERCENTAGE_RANDOM=10
fi

SETTINGS='{"consumer_per_minute":100,"amount_of_consumers":1,"probability_of_buy":100,"min_buying_amount":1,"max_buying_amount":1,"min_wait":0.1,"max_wait":2,"behaviors":[{"name":"first","description":"I am buying the first possible item","settings":{},"settings_description":"Behavior settings not necessary","amount":0},{"name":"random","description":"I am buying random items","settings":{},"settings_description":"Behavior settings not necessary","amount":'$PERCENTAGE_RANDOM'},{"name":"cheap","description":"I am buying the cheapest item","settings":{},"settings_description":"Behavior settings not necessary","amount":'$PERCENTAGE_CHEAPEST'},{"name":"expensive","description":"I am buying the most expensive item","settings":{},"settings_description":"Behavior settings not necessary","amount":0},{"name":"cheap_and_prime","description":"I am buying the cheapest item which supports prime shipping","settings":{},"settings_description":"Behavior settings not necessary","amount":0},{"name":"cheapest_best_quality","description":"I am buying the cheapest best quality available.","settings":{},"settings_description":"Behavior settings not necessary","amount":0},{"name":"cheapest_best_quality_with_prime","description":"I am buying the cheapest best quality available which supports prime.","settings":{},"settings_description":"Behavior settings not necessary","amount":0},{"name":"second_cheap","description":"I am buying the second cheapest item","settings":{},"settings_description":"Behavior settings not necessary","amount":'$PERCENTAGE_SEC_CHEAPEST'},{"name":"third_cheap","description":"I am buying the third cheapest item","settings":{},"settings_description":"Behavior settings not necessary","amount":0},{"name":"sigmoid_distribution_price","description":"I am with sigmoid distribution on the price regarding the producer prices","settings":{},"settings_description":"Behavior settings not necessary","amount":0},{"name":"logit_coefficients","description":"I am with logit coefficients","settings":{"coefficients":{"intercept":-6.6177961,"price_rank":0.2083944,"amount_of_all_competitors":0.253481,"average_price_on_market":-0.0079326,"quality_rank":-0.1835972}},"settings_description":"Key Value map for Feature and their coeffient","amount":'$PERCENTAGE_LOGIT'}],"timeout_if_no_offers_available":2,"timeout_if_too_many_requests":30,"max_buying_price":80,"debug":false,"producer_url":"http://producer:3050","product_popularity":{"1":100},"marketplace_url":"http://marketplace:8080"}'

printf "Setting consumer behaviour to $PERCENTAGE_CHEAPEST%% cheapest, $PERCENTAGE_SEC_CHEAPEST%% second cheapest, $PERCENTAGE_LOGIT%% logit, and $PERCENTAGE_RANDOM%% random: "
RET=`curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: application/json" -d "$SETTINGS" http://consumer:3000/setting`

if [ "$RET" = "200" ]
then
  echo 'successful.'
else
  echo 'unsuccessful.'
fi
