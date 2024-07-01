import hashlib
import datetime as date
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import sys
from uuid import uuid4

import json

from flask import Flask, jsonify, request

from Blockchain import Block, Blockchain

URL = "127.0.0.1"

app = Flask(__name__)
nodce_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

def next_block(last_block: Block, data: str) -> Block:
    return Block(date.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), data, last_block.hash, last_block.nonce)

@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    try:
        data = request.form["data"]
    except:
        return "Data was not sent.", 400

    blockchain.resolve_conflicts()
    new_block = next_block(blockchain.get_last_block(), data)
    if (blockchain.new_block(new_block)):
        return "Tampering with the blockchain was detected.", 500
    
    response = {"message": f"Transaction will be added to Block {len(blockchain.chain)}"}
    return response, 200

@app.route("/chain", methods=["GET"])
def get_full_chain():
    if (not (request.headers.get("referer") == URL)):
        blockchain.resolve_conflicts()

    chain = []
    for block in blockchain.chain:
        dict = {
            "timestamp": str(block.timestamp),
            "data": str(block.data),
            "prev_hash": str(block.prev_hash),
            "nonce": str(block.nonce),
            "hash": str(block.hash),
            "sig": base64.b64encode(block.sig).decode(),
            "pub_key": base64.b64encode(RSA.RsaKey.export_key(block.pub_key)).decode()
        }
        chain.append(dict)
        
    response = {
        "chain": chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    values = request.get_json()

    nodes = values.get("nodes")
    if (nodes is None):
        return "Error: Please supply a valid list of nodes", 400
    
    for node in nodes:
        blockchain.register_node(node)
    
    response = {
        "message": "New nodes have been added",
        "total_nodes": list(blockchain.nodes),
    }
    return jsonify(response), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
