import argparse
import os
from os.path import dirname
import subprocess
import time
import json
import datetime

import requests
from kafka import KafkaConsumer

class PopenWrapper:
    """
    This class is a context manager that wraps subprocess.Popen.
    Popen waits until the created process is finished when exiting the context.
    This wrapper additionaly sends a terminate signal to the program before waiting for it to finish.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        self.process = subprocess.Popen(*self.args, **self.kwargs)
        return self.process

    def __exit__(self, *args):
        self.process.terminate()
        self.process.__exit__(*args)


def dump_topic(topic, output_dir):
    consumer = KafkaConsumer(topic,
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer_timeout_ms=100,
        auto_offset_reset='earliest')

    events = []
    for message in consumer:
        events.append(message.value)
    with open(os.path.join(output_dir, topic), 'w') as file:
        json.dump(events, file)

def dump_kafka(output_dir):
    kafka_dir = os.path.join(output_dir, 'kafka')
    os.mkdir(kafka_dir)
    topics = ['buyOffer', 'holding_cost', 'marketSituation', 'producer']
    for topic in topics:
        dump_topic(topic, kafka_dir)

def profit(output_dir, merchant_id_mapping):
    # read buyOffer -> amount * price
    # read holding_cost -> cost
    # read producer -> billing_amount
    profit = {}
    for merchant_name in merchant_id_mapping.values():
        profit[merchant_name] = 0

    with open(os.path.join(output_dir, 'kafka', 'buyOffer')) as file:
        for event in json.load(file):
            merchant_name = merchant_id_mapping[event['merchant_id']]
            profit[merchant_name] += event['amount'] * event['price']

    with open(os.path.join(output_dir, 'kafka', 'holding_cost')) as file:
        for event in json.load(file):
            merchant_name = merchant_id_mapping[event['merchant_id']]
            profit[merchant_name] -= event['cost']

    with open(os.path.join(output_dir, 'kafka', 'producer')) as file:
        for event in json.load(file):
            merchant_name = merchant_id_mapping[event['merchant_id']]
            profit[merchant_name] -= event['billing_amount']
    
    with open(os.path.join(output_dir, 'profit.json'), 'w') as file:
        json.dump(profit, file)

def save_merchant_name_id_mapping(output_dir):
    merchants_info = requests.get('http://marketplace:8080/merchants').json()
    merchant_mapping = {}
    for merchant_info in merchants_info:
        merchant_mapping[merchant_info['merchant_id']] = merchant_info['merchant_name']
    with open(os.path.join(output_dir, 'merchant_id_mapping.json'), 'w') as file:
        json.dump(merchant_mapping, file)
    return merchant_mapping

def analyze(output_dir):
    os.mkdir(output_dir)
    dump_kafka(output_dir)
    merchant_id_mapping = save_merchant_name_id_mapping(output_dir)
    profit(output_dir, merchant_id_mapping)
    

def clear_container_state(pricewars_dir):
    # This code works only on Linux and Mac
    # Use shutil.rmtree instead
    # Problem with rmtree: no permission to delete directory
    command = 'sudo rm -rf'
    directory = os.path.join(pricewars_dir, 'docker-mounts')
    print('Run:', command, directory)
    subprocess.run(command.split() + [directory])

parser = argparse.ArgumentParser(
    description='Runs a simulation on the Pricewars platform',
    epilog='Usage example: python3 %(prog)s --duration 5 --output ~/results')
parser.add_argument('--duration', '-d', metavar='MINUTES', type=float, required=True, help='Run that many minutes')
parser.add_argument('--output', '-o', metavar='DIRECTORY', type=str, required=True)
args = parser.parse_args()
duration_in_minutes = args.duration
output_dir = os.path.join(args.output, datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S%z"))
if not os.path.isdir(args.output):
    print(args.output, 'is not a directory')
    exit(1)

pricewars_dir = dirname(dirname(os.path.abspath(__file__)))
clear_container_state(pricewars_dir)

with PopenWrapper(['docker-compose', 'up'], cwd=pricewars_dir) as docker:
    # wait until containers are up and running
    # TODO: find a better way to check if platform is ready
    time.sleep(35)

    # TODO: configure marketplace (holding cost)

    # TODO: stop simulation when consumer or merchant crashed
    print('Starting consumer')
    # TODO: provide program and arguments via start parameters
    consumer = subprocess.Popen(['python3', '/home/carsten/masterarbeit/code/customer.py'])

    print('Starting merchant')
    # TODO: provide program and arguments via start parameters
    merchant = subprocess.Popen(['python3', pricewars_dir + '/merchant/merchant_dyn_programming.py', '--port', '5000'])

    # Run for the given amount of time
    print('Run for', duration_in_minutes, 'minutes')
    time.sleep(duration_in_minutes * 60)

    print('Stopping consumer')
    consumer.terminate()
    consumer.wait()

    print('Stopping merchant')
    merchant.terminate()
    merchant.wait()

    analyze(output_dir)