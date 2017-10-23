# Masterproject Pricewars

This is the meta repository of the Pricewars-masterproject that allows the simulation of a dynamic marketplace similar to online marketplaces like www.amazon.com. Using our simulation, one can test different pricing strategies and assess their performance compared to other pricing strategies.

The simulation is built using a microservice architecture and consists of multiple components representing important players in the simulation. Each component has its own repository and documentation and the links can be found in the following section.

On the master-branch, this repository contains the docker-setup that allows running the simulation locally. On the [gh-pages](https://github.com/hpi-epic/masterproject-pricewars/tree/gh-pages)-branch one can find the swagger-documentation of the REST-APIs of all components.

Due to the current github bug that submodules with dependencies to private repositories cannot be resolved, the github page build process fails, enforcing us to separate the API specification from the submodules for rendering those via [github.io](https://hpi-epic.github.io/masterproject-pricewars/).

The API specification can be found [here](https://hpi-epic.github.io/masterproject-pricewars/).

## Application Overview

| Repository | Branch 	| Status | Description |
|--- |---	|---  |---   |
| [UI](https://github.com/hpi-epic/pricewars-mgmt-ui) | master 	| [ ![Codeship Status for hpi-epic/pricewars-mgmt-ui](https://app.codeship.com/projects/d91a8460-88c2-0134-a385-7213830b2f8c/status?branch=master)](https://app.codeship.com/projects/184009) | Stable |
| [Consumer](https://github.com/hpi-epic/pricewars-consumer) | master 	|  [ ![Codeship Status for hpi-epic/pricewars-consumer](https://app.codeship.com/projects/96f32950-7824-0134-c83e-5251019101b9/status?branch=master)](https://app.codeship.com/projects/180119) | Stable |
| [Producer](https://github.com/hpi-epic/pricewars-producer) | master  | [ ![Codeship Status for hpi-epic/pricewars-producer](https://app.codeship.com/projects/0328e450-88c6-0134-e3d6-7213830b2f8c/status?branch=master)](https://app.codeship.com/projects/184016) | Stable |
| [Marketplace](https://github.com/hpi-epic/pricewars-marketplace) | master 	| [ ![Codeship Status for hpi-epic/pricewars-marketplace](https://app.codeship.com/projects/e9d9b3e0-88c5-0134-6167-4a60797e4d29/status?branch=master)](https://app.codeship.com/projects/184015) | Stable |
| [Merchant](https://github.com/hpi-epic/pricewars-merchant) | master	 | [ ![Codeship Status for hpi-epic/pricewars-merchant](https://app.codeship.com/projects/a7d3be30-88c5-0134-ea9c-5ad89f4798f3/status?branch=master)](https://app.codeship.com/projects/184013) | Stable |
| [Kafka RESTful API](https://github.com/hpi-epic/pricewars-kafka-rest) | master 	|  [ ![Codeship Status for hpi-epic/pricewars-kafka-rest](https://app.codeship.com/projects/f59aa150-92f0-0134-8718-4a1d78af514c/status?branch=master)](https://app.codeship.com/projects/186252) | Stable |

## FMC Diagram

![alt tag](/docs/modeling/architecture_fmc.png?raw=true)

## Sequence Diagram

![alt tag](/docs/modeling/sequence_diagram_flow.png?raw=true)

## Deployment

### Docker

#### Clone the repo including all submodules
If you are working on Windows, make sure to set the following git-settings:
```
git config --global core.eol lf
git config --global core.autocrlf input
```
The first setting will ensure that files keep their lf-line endings when checking out a repository.
Otherwise the line endings of all files will be converted to cr+lf under Windows, causing problems with script-execution within the Docker-containers that expect lf-endings.
The second setting ensures that line endings are converted back to what they were on checkout when pushing a change.

*(These settings are global so they will affect all repositories, make sure to change them again if you do not want this behaviour on other repositories!)*

Then go ahead and clone the repository:

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
 - add the following lines (and don't forget additional names if you specify more containers!)

```
127.0.0.1       postgres redis zookeeper kafka kafka-reverse-proxy
127.0.0.1       flink-jobmanager flink-taskmanager analytics management-ui
127.0.0.1       marketplace producer consumer merchant-machine-learning
127.0.0.1       merchant-sample-cheapest merchant-sample-fix-price
127.0.0.1       merchant-sample-random-third merchant-sample-second-cheapest
127.0.0.1       merchant-sample-two-bound merchant-simple-competition-logic1
127.0.0.1       merchant-simple-competition-logic2
```

#### Updating the Docker setup
First, stop your existing containers. In some cases, even though you just pressed `CTRL + C` once, the containers might not be stopped. Additionally, using `CTRL + C` might leave .PID files in some containers that block the containers during the next start. Consequently, we advise to use `docker-compose stop` to stop them all first before continuing (e.g., in another terminal window).

```
docker-compose stop
git pull --recurse-submodules
docker-compose pull --ignore-pull-failures
docker-compose build
docker ps -a | awk '{ print $1,$2 }' | grep $(echo $(docker images --filter "dangling=true" -q) | sed "s/ /\\\\|/g") | awk '{print $1 }' | xargs -I {} docker rm {}
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
docker-compose up
```

#### Windows w/o Docker Native support
For Windows versions that don't have Docker Native support, like Home etc., another solution is to use an Ubuntu virtual machine with Docker installed. We recommend to use Ubuntu Server as the GUI of other Ubuntu versions might consume to much main memory. The main memory should be at least 8GB, since your Windows consumes about 2GB, Ubuntu Server 0.5GB and the simulation about 4GB. Also, your browser will consume a few hundred MB, too.

On your guest system, you have to adjust your DNS settings like mentioned before. If you want to access your simulation from your host system, i.e. with the managment ui in the browser or with a locally deployed merchant, you also need to adjust the DNS settings of this, too. You could also use the Windows Subsystem for Linux (WSL) to run local merchants. Be aware, that you need to adjust the DNS settings a third time, this time in the hosts file of the WSL. Also, you might need to add an exception to your firewall to allow your merchant to access the virtual machine.

#### Help - My Docker Setup is not working as expected!

##### One of the images can't be built:
You might see the following in your console after typing `docker-compose up` for the first time (which will initially build the containers):

```
[warn] 	::::::::::::::::::::::::::::::::::::::::::::::
[warn] 	::          UNRESOLVED DEPENDENCIES         ::
[warn] 	::::::::::::::::::::::::::::::::::::::::::::::
[warn] 	:: pricewars-utils#pricewars-utils_2.11;0.1-SNAPSHOT: not found
[warn] 	::::::::::::::::::::::::::::::::::::::::::::::
[warn]
[warn] 	Note: Unresolved dependencies path:
[warn] 		pricewars-utils:pricewars-utils_2.11:0.1-SNAPSHOT
[warn] 		  +- flinkutils:flinkutils_2.11:1.0
```

Most probably, the utils submodule was not cloned correctly. Check that `analytics\utils` is not empty. Within the `analytics` folder, execute the following command:

```
git submodule update
```
You might need to add an SSH key to your GitHub account in order to clone the repository. Visit the [GitHub Help](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) for more details.

##### Some containers quit unexpectedly:
First, the analytics container is expected to be stopped after a short moment - it's just used to compile and export the flink jobs. If this is the only container not running, you're fine. In case any other container is not running, analyse the first container (except for analytics) that stopped.
- __Postgres__: Either empty the `docker-mounts/postgres` folder (if running on Unix / Linux) or remove mounting a volume to Postgres completly (required on Windows, optional on Unix / Windows).
- __Zookeeper / Kafka__: If you just stopped some older containers: Wait! There is a timeout for Zookeeper to notice that Kafka has been stopped (timestamp-based, so it works even if Zookeeper is not running). Otherwise, first remove the `docker-mounts/zookeeper` folder and try again. If this doesn't work, remove the folder again and `docker-mounts\kafka` in addition (Warning: This will remove the Kafka history).
- __Others__: Try to read the logs or read on.

##### The command `docker-compose up` is hanging:
- Try to remove the `docker-mount` folder and start your containers again.
- Reset the containers and the network: `docker system prune` (and restart the Docker service).
- Terminate Docker and ensure, that all docker processes are stopped (especially the network service).
- Restart your computer and wait (even though it might be slow) for about five to ten minutes.
- Reset Docker to factory defaults (should be your last attempt, as this requires re-building of all images):
 - macOS: Click on "Preferences" > "Reset" > "Reset to factory defaults"

### Continuous Deployment

For the production environment within the HPI cluster, we use [Codeship](http://codeship.com/) for Continuous Integration (CI) & Continuous Deployment (CD). In each repository, there is a _config/deploy/_ folder containing deployment specifications which are executed via [capistrano](https://github.com/capistrano/capistrano).

"Capistrano is a framework for building automated deployment scripts. Although Capistrano itself is written in Ruby, it can easily be used to deploy projects of any language or framework, be it Rails, Java, or PHP. [..] When you run *cap*, Capistrano dutifully connects to your server(s) via SSH and executes the steps necessary to deploy your project. You can define those steps yourself by writing Rake tasks, or by using pre-built task libraries provided by the Capistrano community." [quote](https://github.com/capistrano/capistrano).

In  _config/_, the *deploy.rb* file contains general deployment information like the git repository url, the deployment directory within the target system as well as the deployment tasks executed for each deployment iteration to initiate and setup the environment if necessary.
For each deployment stage, the files in  _config/deploy/_ define additional specifications and steps. Those are the target system destination and port as well as tokens for the merchants and more details. In terms of the target system destination, we route the SSH session via a reverse-port-forwarding setup which again is established through a secure VPN to tunnel into the HPI cluster boundaries.
More details regarding this VPN configuration may be found under _config/openvpn_server/_.



### Native
For details regarding the deployment of the component, we kindly refer to the deployment section of the microservice specific README.md file. The links can be found above.

## Setup

After marketplace, producer and logger are in place, one may

1. Register Merchants via UI (Menu section: Deployment)
2. Alter available product via UI (Menu section: Config/Producer)
3. Start Merchants via UI (Menu section: Config/Merchant)
4. Start Consumer via UI (Menu section: Config/Consumer)
5. View Results via UI (Menu section: Dashboard)
6. In case of performance issues, one may debug bottlenecks with munin graphs (Menu section: Links/Munin)
