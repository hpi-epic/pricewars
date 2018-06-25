import argparse
import os
from os.path import dirname
import subprocess
import time
import json
import datetime
import random
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


def dump_topic(topic, output_dir, kafka_host):
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=kafka_host,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                             consumer_timeout_ms=2000,
                             auto_offset_reset='earliest')

    events = [message.value for message in consumer]
    with open(os.path.join(output_dir, topic), 'w') as file:
        json.dump(events, file)


def dump_kafka(output_dir, kafka_host):
    kafka_dir = os.path.join(output_dir, 'kafka')
    os.mkdir(kafka_dir)
    topics = ['buyOffer', 'holding_cost', 'marketSituation', 'producer']
    for topic in topics:
        dump_topic(topic, kafka_dir, kafka_host)


def save_merchant_id_mapping(output_dir, marketplace_url):
    merchants_info = requests.get(marketplace_url + '/merchants').json()
    merchant_mapping = {}
    for merchant_info in merchants_info:
        merchant_mapping[merchant_info['merchant_id']] = merchant_info['merchant_name']
    with open(os.path.join(output_dir, 'merchant_id_mapping.json'), 'w') as file:
        json.dump(merchant_mapping, file)


def clear_containers(pricewars_dir):
    subprocess.run(['docker-compose', 'rm', '--stop', '--force'], cwd=pricewars_dir)


def set_consumer_ratios(resp, **kwargs):
	behaviors_to_use = {}
	for k, v in kwargs.items():
		behavior = [b for b in resp['behaviors'] if b['name'] == k]

		if len(behavior) == 1:
			behaviors_to_use[k] = v
		else:
			print(f"Unable to set consumer behaviour '{k}': not implemented by consumer.")

	b_sum = sum(behaviors_to_use.values())
	factor = 100 / b_sum
	for k, v in behaviors_to_use.items():
		behaviors_to_use[k] = v*factor

	for b in resp['behaviors']:
		if b['name'] in behaviors_to_use:
			b['amount'] = int(behaviors_to_use[b['name']])
			continue
		b['amount'] = 0

	return resp


def wait_for_marketplace(marketplace_url, timeout=300):
    """
    Send requests to the marketplace until there is a response
    """
    start = time.time()
    while time.time() - start < timeout:
        try:
            requests.get(marketplace_url)
            return
        except requests.exceptions.ConnectionError:
            pass
    raise RuntimeError('Cannot reach marketplace')

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Runs a simulation on the Pricewars platform',
        epilog='Usage example: python3 %(prog)s --duration 5 --output ~/results '
               '--merchants "python3 merchant/merchant.py --port 5000"')
    parser.add_argument('--duration', '-d', metavar='MINUTES', type=float, required=True, help='Run that many minutes')
    parser.add_argument('--output', '-o', metavar='DIRECTORY', type=str, required=True)
    parser.add_argument('--merchants', '-m', metavar='MERCHANT', type=str, nargs='+', required=True,
                        help='commands to start merchants')
    parser.add_argument('--marketplace_url', type=str, default='http://localhost:8080')
    parser.add_argument('--consumer_url', type=str, default='http://localhost:3000')
    parser.add_argument('--kafka_host', type=str, default='localhost:9093')
    parser.add_argument('--holding_cost', type=float, default=0.0)
    return parser.parse_args()

def main():
    pricewars_dir = dirname(dirname(os.path.abspath(__file__)))
    args = parse_arguments()
    duration_in_minutes = args.duration

    if not os.path.isdir(args.output):
        raise RuntimeError('Invalid output directory: ' + args.output)

    output_dir = os.path.join(args.output, datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S%z"))
    os.mkdir(output_dir)
    clear_containers(pricewars_dir)

    # Start all services from the docker-compose file except the merchants.
    core_services = ['producer', 'marketplace', 'management-ui', 'analytics', 'flink-taskmanager', 'flink-jobmanager',
                     'kafka-reverse-proxy', 'kafka', 'zookeeper', 'redis', 'postgres', 'consumer']
    with PopenWrapper(['docker-compose', 'up'] + core_services, cwd=pricewars_dir):
        # configure marketplace
        wait_for_marketplace(args.marketplace_url)
        requests.put(args.marketplace_url + '/holding_cost_rate', json={'rate': args.holding_cost})

        print('Starting consumer')
        consumer_settings = requests.get(args.consumer_url + '/setting').json()
        set_consumer_ratios(consumer_settings, prefer_cheap = random.randint(4, 7),
                                               cheapest_best_quality = random.randint(2, 4))
        response = requests.post(args.consumer_url + '/setting', json=consumer_settings)
        response.raise_for_status()

        print('Starting merchants')
        merchants = [subprocess.Popen(shlex.split(command)) for command in args.merchants]

        # Run for the given amount of time
        print('Run for', duration_in_minutes, 'minutes')
        time.sleep(duration_in_minutes * 60)

        print('Stopping consumer')
        requests.delete(args.consumer_url + '/setting')

        print('Stopping merchants')
        for merchant in merchants:
            merchant.terminate()
            merchant.wait()

        dump_kafka(output_dir, args.kafka_host)
        save_merchant_id_mapping(output_dir, args.marketplace_url)

    analyze_kafka_dump(output_dir)


if __name__ == '__main__':
    main()
