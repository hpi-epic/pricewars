# masterproject-pricewars

## Deployment

### Docker

#### Clone the repo including all submodules
```
git clone git@github.com:hpi-epic/masterproject-pricewars.git --recurse-submodules
cd masterproject-pricewars
docker-compose up
```

#### Disable Volume Mounting for Postgres on Windows!
Postgres in Docker for Windows has a problem accessing the files when they are mounted from a volume.
Just add a hash # in front of the "volumes:" and "- ./docker-mounts/postgres:/var/lib/postgresql/data" line

#### Adjust some DNS settings:
 - open "/etc/hosts" as root on Linux / Unix or "C:\Windows\System32\drivers\etc\hosts" on Windows as Administrator
 - add the following lines (and don't forget aditional names if you specify more containers!)

```
127.0.0.1       postgres redis zookeeper kafka kafka-reverse-proxy 
127.0.0.1       flink-jobmanager flink-taskmanager analytics management-ui 
127.0.0.1       marketplace producer consumer merchant-machine-learning 
127.0.0.1       merchant-sample-cheapest merchant-sample-fix-price 
127.0.0.1       merchant-sample-random-third merchant-sample-second-cheapest 
127.0.0.1       merchant-sample-two-bound merchant-simple-competition-logic1 
127.0.0.1       merchant-simple-competition-logic2
```
   
### Native
For details regarding the deployment of the component, we kindly refer to the deployment section of the microservice specific README.md file. The links can be found below.

## Setup

After marketplace, producer and logger are in place, one may

1. Register Merchants via UI (Menu section: Deployment)
2. Alter available product via UI (Menu section: Config/Producer)
3. Start Merchants via UI (Menu section: Config/Merchant)
4. Start Consumer via UI (Menu section: Config/Consumer)
5. View Results via UI (Menu section: Dashboard)
6. In case of performance issues, one may debug bottlenecks with munin graphs (Menu section: Links/Munin)


## Application Overview

| Repo | Branch 	| Deployment to  	| Status | Description |
|--- |---	|---	|---  |---   |
| [UI](https://github.com/hpi-epic/pricewars-mgmt-ui) | master  	|  [vm-mpws2016hp1-02.eaalab.hpi.uni-potsdam.de](http://vm-mpws2016hp1-02.eaalab.hpi.uni-potsdam.de) 	| [ ![Codeship Status for hpi-epic/pricewars-mgmt-ui](https://app.codeship.com/projects/d91a8460-88c2-0134-a385-7213830b2f8c/status?branch=master)](https://app.codeship.com/projects/184009) | Stable |
| [Consumer](https://github.com/hpi-epic/pricewars-consumer) | master  	|  [vm-mpws2016hp1-01.eaalab.hpi.uni-potsdam.de](http://vm-mpws2016hp1-01.eaalab.hpi.uni-potsdam.de) | [ ![Codeship Status for hpi-epic/pricewars-consumer](https://app.codeship.com/projects/96f32950-7824-0134-c83e-5251019101b9/status?branch=master)](https://app.codeship.com/projects/180119) | Stable |
| [Producer](https://github.com/hpi-epic/pricewars-producer) | master  	|  [vm-mpws2016hp1-03eaalab.hpi.uni-potsdam.de](http://vm-mpws2016hp1-03.eaalab.hpi.uni-potsdam.de) | [ ![Codeship Status for hpi-epic/pricewars-producer](https://app.codeship.com/projects/0328e450-88c6-0134-e3d6-7213830b2f8c/status?branch=master)](https://app.codeship.com/projects/184016) | Stable |
| [Marketplace](https://github.com/hpi-epic/pricewars-marketplace) | master  	|  [vm-mpws2016hp1-04.eaalab.hpi.uni-potsdam.de/marketplace](http://vm-mpws2016hp1-04.eaalab.hpi.uni-potsdam.de/marketplace/offers) 	| [ ![Codeship Status for hpi-epic/pricewars-marketplace](https://app.codeship.com/projects/e9d9b3e0-88c5-0134-6167-4a60797e4d29/status?branch=master)](https://app.codeship.com/projects/184015) | Stable |
| [Merchant](https://github.com/hpi-epic/pricewars-merchant) | master  	|  [vm-mpws2016hp1-06.eaalab.hpi.uni-potsdam.de/](http://vm-mpws2016hp1-06.eaalab.hpi.uni-potsdam.de/) 	| [ ![Codeship Status for hpi-epic/pricewars-merchant](https://app.codeship.com/projects/a7d3be30-88c5-0134-ea9c-5ad89f4798f3/status?branch=master)](https://app.codeship.com/projects/184013) | Stable |
| [Kafka RESTful API](https://github.com/hpi-epic/pricewars-kafka-rest) | master  	|  [vm-mpws2016hp1-05.eaalab.hpi.uni-potsdam.de](http://vm-mpws2016hp1-05.eaalab.hpi.uni-potsdam.de) 	|  [ ![Codeship Status for hpi-epic/pricewars-kafka-rest](https://app.codeship.com/projects/f59aa150-92f0-0134-8718-4a1d78af514c/status?branch=master)](https://app.codeship.com/projects/186252) | Stable |

## API Specification

The API specification can be found [here](https://hpi-epic.github.io/masterproject-pricewars/api/#/).

## FMC Diagram

![alt tag](/docs/modeling/architecture_fmc.png?raw=true)

## Sequence Diagram

![alt tag](/docs/modeling/sequence_diagram_flow.png?raw=true)
