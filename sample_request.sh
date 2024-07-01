#! /bin/bash

# set -x

curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://192.168.1.3:5000"]
}' "http://localhost:5000/nodes/register"

curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://192.168.1.4:5000"]
}' "http://localhost:5000/nodes/register"

curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://192.168.1.2:5000"]
}' "http://localhost:5001/nodes/register"

curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://192.168.1.4:5000"]
}' "http://localhost:5001/nodes/register"

curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://192.168.1.2:5000"]
}' "http://localhost:5002/nodes/register"

curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://192.168.1.3:5000"]
}' "http://localhost:5002/nodes/register"

# block: 2
curl -X POST -F "data=data1" http://localhost:5000/transactions/new

# block: 3
curl -X POST -F "data=data2" http://localhost:5001/transactions/new

# block: 4
curl -X POST -F "data=data3" http://localhost:5002/transactions/new

# block: 4
curl -X POST -F "data=data2" http://localhost:5001/transactions/new

# get current ledger
curl http://localhost:5000/chain | jq

curl http://localhost:5000/chain | jq > 5000.tmp

curl http://localhost:5001/chain | jq > 5001.tmp

curl http://localhost:5001/chain | jq > 5002.tmp

diff 5000.tmp 5001.tmp && diff 5001.tmp 5002.tmp && echo "Ledgers are synchronized"
rm 500[012].tmp
