<img alt="Price Wars" width="50%" src="/docs/pricewars_logo.svg">

# A Simulation Platform for Dynamic Pricing Competition


Currently, retailers lack the possibility to test, develop, and evaluate their algorithms appropriately before releasing them into the real world. At the same time, it is challenging for researchers to investigate how pricing strategies interact with each other under heavy competition.

We built an open platform to simulate dynamic pricing competition allowing both practitioners and researchers to study the effects of automated repricing mechanisms competing with each other using market scenarios that mimic real-world marketplaces.

We built the platform in a way that one can participate and deploy own merchants with only a few lines of Python code. It allows merchants to deploy the full width of pricing strategies, from simple rule-based strategies to more sophisticated data-driven strategies using machine learning. For practitioners, the platform further provides a possibility to evaluate their pricing strategies appropriately before releasing them in production.

For more information about the platform and publications, see the our chair's [project site](https://hpi.de/en/plattner/projects/price-wars-an-interactive-simulation-platform.html) on Dynamic Pricing under Competition.

On the master branch, this repository contains the docker-setup that allows running the simulation locally. On the [gh-pages](https://github.com/hpi-epic/pricewars/tree/gh-pages) branch one can find the [API specification](https://hpi-epic.github.io/pricewars/) of all components.

## Application Overview

**Repositories**
* Management UI: [https://github.com/hpi-epic/pricewars-mgmt-ui](https://github.com/hpi-epic/pricewars-mgmt-ui)
* Consumer: [https://github.com/hpi-epic/pricewars-consumer](https://github.com/hpi-epic/pricewars-consumer)
* Producer: [https://github.com/hpi-epic/pricewars-producer](https://github.com/hpi-epic/pricewars-producer)
* Marketplace: [https://github.com/hpi-epic/pricewars-marketplace](https://github.com/hpi-epic/pricewars-marketplace)
* Merchant: [https://github.com/hpi-epic/pricewars-merchant](https://github.com/hpi-epic/pricewars-merchant)
* Kafka RESTful API: [https://github.com/hpi-epic/pricewars-kafka-rest](https://github.com/hpi-epic/pricewars-kafka-rest)
* Analytics: [https://github.com/hpi-epic/pricewars-analytics](https://github.com/hpi-epic/pricewars-analytics)

## Architecture

![FMC Architecture Diagram](/docs/modeling/pricewars-architecture.png?raw=true)

## Sequence Diagram

![Sequence Diagram](/docs/modeling/sequence_diagram_flow.png?raw=true)

## Deployment

### Requirements

* [Docker](https://www.docker.com/)
  * If you are on Linux read [this](https://docs.docker.com/install/linux/linux-postinstall/) for running docker as non-root user.
* [Docker Compose](https://docs.docker.com/compose/install/)

### Setup
Clone the repository and its subrepositories:

```
git clone --recursive git@github.com:hpi-epic/pricewars.git
```

For the next step bring a fast internet line and some time.
This can take up to 30 minutes at the first-time setup.
Build docker images and containers with the following command.

```
cd pricewars
docker-compose build
```

### Run Price Wars

The Price Wars platform can be started with:

```
docker-compose up
```

This will start all services and one example merchant.
You can shut down the platform with `CTRL + C` or `docker-compose stop`.

Warning: There might be routing problems if the docker network overlaps with your local network.
If this is the case, change the ip address in `docker-compose.yml` under the `networks` entry.

After starting the Pricewars platform with `docker-compose up`, it can be controlled with the [Management UI](http://localhost)

1. \[Optional] Configure available products in the [Config/Producer section](http://localhost/index.html#/config/producer)
2. Start the [Consumer](http://localhost/index.html#/config/consumer)
3. Merchants are trading products now. The [Dashboard](http://localhost/index.html#/dashboard/overview) shows graphs about sales, profits and more.

In the [Merchant repository](https://github.com/hpi-epic/pricewars-merchant) you can learn how to build your own merchant and run it on the platform.

#### Cleaning up containers and existing state
Run the following commands to run the platform in a clean state.

```
docker-compose down
docker-compose up
```

#### Updating the Docker setup
First, stop your running containers.

```
docker-compose stop
```

Update repositories.
```
git pull
git submodule update
```

Rebuild all images that have changed:
```
docker-compose build
```

#### Help - My Docker Setup is not working as expected!

##### Some containers quit unexpectedly:
You can see the status of the containers with `docker-compose ps`.
In case a container is not running, you can see its last logs with `docker-compose logs <service name>`.
- __Postgres__: Bring the platform in a clean state with `docker-compose down` and run it again.
- __Zookeeper / Kafka__: If you just stopped some older containers: Wait! There is a timeout for Zookeeper to notice that Kafka has been stopped (timestamp-based, so it works even if Zookeeper is not running). Bring the platform in a clean state with `docker-compose rm --stop` and run it again.
- __Others__: Try to read the logs or read on.

##### The command `docker-compose up` is hanging:
- Reset the containers and the network: `docker system prune` (and restart the Docker service).
- Terminate Docker and ensure, that all docker processes are stopped (especially the network service).
- Restart your computer and wait (even though it might be slow) for about five to ten minutes.
- Reset Docker to factory defaults (should be your last attempt, as this requires re-building of all images):
 - macOS: Click on "Preferences" > "Reset" > "Reset to factory defaults"

### Native
For details regarding the deployment of the component, we kindly refer to the deployment section of the microservice specific README.md file. The links can be found above.

## Benchmark Tool

You can run a benchmark on the Price Wars platform with the benchmark tool [benchmark.py](helper_scripts/benchmark.py).
This tool allows to run the platform in a given configuration for a specific time period.
Afterwards, results of this run are written to the output directory.

Firstly, install necessary Python libraries:
```
python3 -m pip install -r helper_scripts/requirements.txt
```

Example command:
```
python3 helper_scripts/benchmark.py --duration 30 --output <output directory> --merchants <merchant A command> <merchant B command>
```

This starts the whole platform and two merchants to compete against each other for 30 minutes.
As merchant start command you can use for example: `"python3 merchant/merchant.py --strategy cheapest --port 5000"`.
The quotes must be included.
Run `python3 helper_scripts/benchmark.py --help` to see all arguments.

## Developement
There are different ways to develop the containerized marketplace services. These approaches have different trade-offs between setup time and time to run the platform with the new code.

#### Rebuilding the docker image
This method does not require any extra setup. The workflow is to modify code, then rebuild the docker images. Use the following commands:
```
docker-compose down
docker rmi <name_of_image>
```
On the next start of the platform, the new image will be built.

Rebuilding an image takes a few seconds up to over a minute depending on the service.

#### Mounting a volume
If rebuilding the image to too tedious, an alternative approach is mounting the executable (or source code) onto the docker container. This way, the program can be built locally and is used by the container on the next start.

The directory can be mounted in the `docker-compose.yml` file with the `volumes` option. 

#### Run service natively
It is possible to run a service natively. This removes the docker abstraction and is the fastest way to restart the service with a new version.

However, the service must be reconfigured to connect to the docker services and vice versa.

Visit the corresponding subrepository on how to run a service natively and how to configure it.
