import argparse
import os
from os.path import dirname
import subprocess
import time
import json
import datetime
import shlex

import requests
from kafka import KafkaConsumer

from analyze import analyze_kafka_dump


class PopenWrapper:
    """
    This class is a context manager that wraps subprocess.Popen.
    Popen waits until the created process is finished when exiting the context.
    This wrapper additionally sends a terminate signal to the program before waiting for it to finish.
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
                             consumer_timeout_ms=2000,
                             auto_offset_reset='earliest')

    events = [message.value for message in consumer]
    with open(os.path.join(output_dir, topic), 'w') as file:
        json.dump(events, file)


def dump_kafka(output_dir):
    kafka_dir = os.path.join(output_dir, 'kafka')
    os.mkdir(kafka_dir)
    topics = ['buyOffer', 'holding_cost', 'marketSituation', 'producer']
    for topic in topics:
        dump_topic(topic, kafka_dir)


def save_merchant_id_mapping(output_dir):
    merchants_info = requests.get('http://marketplace:8080/merchants').json()
    merchant_mapping = {}
    for merchant_info in merchants_info:
        merchant_mapping[merchant_info['merchant_id']] = merchant_info['merchant_name']
    with open(os.path.join(output_dir, 'merchant_id_mapping.json'), 'w') as file:
        json.dump(merchant_mapping, file)


def clear_containers(pricewars_dir):
    subprocess.run(['docker-compose', 'rm', '--stop', '--force'], cwd=pricewars_dir)


def wait_for_marketplace(timeout=60):
    """
    Send requests to the marketplace until there is a response
    """
    start = time.time()
    while time.time() - start < timeout:
        try:
            requests.get('http://marketplace:8080')
            return
        except requests.exceptions.ConnectionError:
            pass
    raise RuntimeError('Cannot reach marketplace')


def main():
    pricewars_dir = dirname(dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(
        description='Runs a simulation on the Pricewars platform',
        epilog='Usage example: python3 %(prog)s --duration 5 --output ~/results'
               '--merchants "python3 merchant/merchant.py --port 5000" --consumer "python3 consumer/consumer.py"')
    parser.add_argument('--duration', '-d', metavar='MINUTES', type=float, required=True, help='Run that many minutes')
    parser.add_argument('--output', '-o', metavar='DIRECTORY', type=str, required=True)
    parser.add_argument('--merchants', '-m', metavar='MERCHANT', type=str, nargs='+', required=True,
                        help='commands to start merchants')
    parser.add_argument('--consumer', '-c', type=str, required=True, help='command to start consumer')
    parser.add_argument('--holding_cost', type=float, default=0.0)
    args = parser.parse_args()
    duration_in_minutes = args.duration

    if not os.path.isdir(args.output):
        raise RuntimeError('Invalid output directory: ' + args.output)

    output_dir = os.path.join(args.output, datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S%z"))
    os.mkdir(output_dir)
    clear_containers(pricewars_dir)

    core_services = ['producer', 'marketplace', 'management-ui', 'analytics', 'flink-taskmanager', 'flink-jobmanager',
                     'kafka-reverse-proxy', 'kafka', 'zookeeper', 'redis', 'postgres']
    with PopenWrapper(['docker-compose', 'up'] + core_services, cwd=pricewars_dir):
        # wait until the marketplace service is up and running
        wait_for_marketplace()

        # configure marketplace
        requests.put('http://marketplace:8080/holding_cost_rate', json={'rate': args.holding_cost})

        print('Starting consumer')
        consumer = subprocess.Popen(shlex.split(args.consumer))

        print('Starting merchants')
        merchants = [subprocess.Popen(shlex.split(command)) for command in args.merchants]

        # Run for the given amount of time
        print('Run for', duration_in_minutes, 'minutes')
        time.sleep(duration_in_minutes * 60)

        print('Stopping consumer')
        consumer.terminate()
        consumer.wait()

        print('Stopping merchants')
        for merchant in merchants:
            merchant.terminate()
            merchant.wait()

        dump_kafka(output_dir)
        save_merchant_id_mapping(output_dir)

    analyze_kafka_dump(output_dir)


if __name__ == '__main__':
    main()
