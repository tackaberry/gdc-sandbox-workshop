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

## Labs

* [Lab 1 - Deploy HTML Server](./LAB-1.md)
* [Lab 2 - Deploy API Server](./LAB-2.md)
* [Lab 3 - Deploy Elasticsearch](./LAB-3.md)