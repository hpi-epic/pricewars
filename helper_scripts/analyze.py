"""
Analyzes the dump of kafka data, that was created by benchmark.py.
Results (e.g. a merchant's profit and revenue) are saved to a CSV file.
"""

import csv
import os
import json
from collections import defaultdict


def load_merchant_id_mapping(directory):
    with open(os.path.join(directory, 'merchant_id_mapping.json')) as file:
        return json.load(file)


def analyze_kafka_dump(directory):
    merchant_id_mapping = load_merchant_id_mapping(directory)

    revenue = defaultdict(float)
    with open(os.path.join(directory, 'kafka', 'buyOffer')) as file:
        for event in json.load(file):
            revenue[event['merchant_id']] += event['amount'] * event['price']

    holding_cost = defaultdict(float)
    with open(os.path.join(directory, 'kafka', 'holding_cost')) as file:
        for event in json.load(file):
            holding_cost[event['merchant_id']] += event['cost']

    order_cost = defaultdict(float)
    with open(os.path.join(directory, 'kafka', 'producer')) as file:
        for event in json.load(file):
            order_cost[event['merchant_id']] += event['billing_amount']

    profit = {merchant_id: revenue[merchant_id] - holding_cost[merchant_id] - order_cost[merchant_id]
              for merchant_id in merchant_id_mapping}

    with open(os.path.join(directory, 'results.csv'), 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'revenue', 'holding_cost', 'order_cost', 'profit'])
        for merchant_id in sorted(merchant_id_mapping, key=merchant_id_mapping.get):
            writer.writerow([merchant_id_mapping[merchant_id], revenue[merchant_id], holding_cost[merchant_id],
                             order_cost[merchant_id], profit[merchant_id]])
