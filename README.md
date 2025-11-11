# GDC Sandbox Workshop

## Setup

1. Clone the repo locally. 

2. Edit the `.env` file. 
```bash

cd ~/gdc-sandbox-workshop
cp .env.example .env

# edit .env for specifics
vi .env

source .env
```

3. Copy the `.env` file to sandbox. 
```bash
./sandbox.sh env
```

## Lab 1 - Deploy HTML Server

For context, we'll review ku alias, build script, and kustomization. 

1. On sandbox, login. 

Confirm `.env` settings. 

```bash
cat .env
```

Login

```bash
cd ~/gdc-sandbox-workshop
source .env
login
```

2. Build and deploy service

```bash
build ./workloads/web-server/app web-server
# show harbor

ku apply -k web-server/base/cluster
```

Inspect
```bash
ku get pods
ku get svc
```
Get webserver ip address
```bash
export WEBSERVER_IP=$(ku get svc -l app-name=web-server -o jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}')
echo $WEBSERVER_IP
echo "curl -X GET http://$WEBSERVER_IP"
```

3. Test over ssh

```bash
curl -X GET http://<ipaddress>
```
