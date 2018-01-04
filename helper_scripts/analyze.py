"""
Reads the dump of kafka data, that was created by benchmark.py, analyzes the data and
saves the results to the same directory
"""

import csv
import os
import json


def analyze_kafka_dump(directory):
    merchant_id_mapping = load_merchant_id_mapping(directory)
    calculate_profit(directory, merchant_id_mapping)


def load_merchant_id_mapping(directory):
    with open(os.path.join(directory, 'merchant_id_mapping.json')) as file:
        return json.load(file)


def calculate_profit(directory, merchant_id_mapping):
    profit = {}
    for merchant_name in merchant_id_mapping.values():
        profit[merchant_name] = 0

    with open(os.path.join(directory, 'kafka', 'buyOffer')) as file:
        for event in json.load(file):
            merchant_name = merchant_id_mapping[event['merchant_id']]
            profit[merchant_name] += event['amount'] * event['price']

    with open(os.path.join(directory, 'kafka', 'holding_cost')) as file:
        for event in json.load(file):
            merchant_name = merchant_id_mapping[event['merchant_id']]
            profit[merchant_name] -= event['cost']

    with open(os.path.join(directory, 'kafka', 'producer')) as file:
        for event in json.load(file):
            merchant_name = merchant_id_mapping[event['merchant_id']]
            profit[merchant_name] -= event['billing_amount']

    with open(os.path.join(directory, 'profit.csv'), 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'profit'])
        writer.writerows(profit.items())