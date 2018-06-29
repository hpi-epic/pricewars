"""
Analyzes the dump of kafka data, that was created by benchmark.py.
Results (e.g. a merchant's profit and revenue) are saved to a CSV file.
"""

import argparse
import csv
import datetime
import os
import json
from collections import defaultdict

import matplotlib
matplotlib.use('Agg') # required for headless plotting

import matplotlib.pyplot as plt


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

    create_inventory_graph(directory, merchant_id_mapping)
    create_profit_per_minute_graph(directory, merchant_id_mapping)
    create_revenue_per_minute_graph(directory, merchant_id_mapping)

def parse_timestamps(events):
    for event in events:
        # TODO: ues better conversion; strptime discards timezone
        try:
            event['timestamp'] = datetime.datetime.strptime(event['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            # Dates in topic 'inventory_level' have no milliseconds
            event['timestamp'] = datetime.datetime.strptime(event['timestamp'], '%Y-%m-%dT%H:%M:%SZ')

def create_inventory_graph(directory, merchant_id_mapping):
    inventory_events = json.load(open(os.path.join(directory, 'kafka', 'inventory_level')))
    parse_timestamps(inventory_events)
    fig, ax = plt.subplots()
    for merchant_id in merchant_id_mapping:
        dates, inventory_levels = zip(*((event['timestamp'], event['level']) for event
            in inventory_events if event['merchant_id'] == merchant_id))
        ax.step(dates, inventory_levels, where='post', label=merchant_id_mapping[merchant_id])
    plt.xlabel('Time')
    plt.ylabel('Inventory Level')
    fig.legend()
    fig.autofmt_xdate()
    fig.savefig(os.path.join(directory, 'inventory_levels'))

def create_profit_per_minute_graph(directory, merchant_id_mapping):
    events = json.load(open(os.path.join(directory, 'kafka', 'profitPerMinute')))
    parse_timestamps(events)
    fig, ax = plt.subplots()
    for merchant_id in merchant_id_mapping:
        dates, profits = zip(*((event['timestamp'], event['profit']) for event
            in events if event['merchant_id'] == merchant_id))
        ax.plot(dates, profits, label=merchant_id_mapping[merchant_id])
    plt.xlabel('Time')
    plt.ylabel('Profit per Minute')
    fig.legend()
    fig.autofmt_xdate()
    fig.savefig(os.path.join(directory, 'profit_per_minute'))

def create_revenue_per_minute_graph(directory, merchant_id_mapping):
    events = json.load(open(os.path.join(directory, 'kafka', 'revenuePerMinute')))
    parse_timestamps(events)
    fig, ax = plt.subplots()
    for merchant_id in merchant_id_mapping:
        dates, revenues = zip(*((event['timestamp'], event['revenue']) for event
            in events if event['merchant_id'] == merchant_id))
        ax.plot(dates, revenues, label=merchant_id_mapping[merchant_id])
    plt.xlabel('Time')
    plt.ylabel('Revenue per Minute')
    fig.legend()
    fig.autofmt_xdate()
    fig.savefig(os.path.join(directory, 'revenue_per_minute'))


def main():
    parser = argparse.ArgumentParser(description='Analyzes the data generated by benchmark.py')
    parser.add_argument('--directory', '-d', type=str, required=True)
    args = parser.parse_args()
    analyze_kafka_dump(args.directory)


if __name__ == '__main__':
    main()
