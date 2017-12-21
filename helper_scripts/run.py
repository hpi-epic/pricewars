import argparse
import os
from os.path import dirname
import subprocess
import time

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

def clear_container_state(pricewars_root_dir):
    command = 'sudo rm -rf'
    directory = os.path.join(pricewars_root_dir, 'docker-mounts')
    print('Run:', command, directory)
    subprocess.run(command.split() + [directory])

parser = argparse.ArgumentParser(description='Runs a simulation on the Pricewars platform',
    epilog='Usage example: python3 run.py --duration 5')
parser.add_argument('--duration', '-d', metavar='MINUTES', type=float, required=True, help='Run that many minutes')
args = parser.parse_args()
duration_in_minutes = args.duration

pricewars_root_dir = dirname(dirname(os.path.abspath(__file__)))
clear_container_state(pricewars_root_dir)

with PopenWrapper(['docker-compose', 'up'], cwd=pricewars_root_dir) as docker:
    # wait until containers are up and running
    time.sleep(35)

    # configure producer
    # not yet implemented

    # start/configure consumers
    print('Starting consumers')
    consumer = subprocess.Popen(['python3', '/home/carsten/masterarbeit/code/customer.py'])

    # start merchants
    print('Starting merchants')
    # currently automatically started by docker-compose up
    # TODO: don't start merchants in docker-compose.yml

    # Run for the given amount of time
    print('Run for', duration_in_minutes, 'minutes')
    time.sleep(duration_in_minutes * 60)

    # stop consumer
    print('Stop consumer')
    consumer.terminate()
    consumer.wait()