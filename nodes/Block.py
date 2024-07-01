from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import hashlib
import random

class Block:
    __hash_zeros = 4

    def __init__(self, timestamp: str, data: str, prev_hash: str, prev_nonce: int = None, nonce: int = None, hash: str = None, sig: bytes = None, pub_key: bytes = None) -> None:
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash

        if (nonce is None):
            self.nonce = self.proof_of_work(prev_nonce)
        else:
            self.nonce = nonce

        if (hash is None):
            self.hash = self.hash_block()
        else:
            self.hash = hash

        if (sig is None):
            self.sig = self.sign()
        else:
            self.sig = sig

        if (pub_key is None):
            with open('public-key.pem', 'br') as f:
                public_key = RSA.import_key(f.read())
            self.pub_key = public_key
        else:
            self.pub_key = RSA.import_key(pub_key)

    
    def proof_of_work(self, last_proof: int) -> int:
        proof = random.randint(0, 10000000)
        while (not self.is_valid_proof(last_proof, proof)):
            proof += 1
        return proof
    
    @staticmethod
    def is_valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return (guess_hash[:Block.__hash_zeros] == '0'*Block.__hash_zeros)
        
    def hash_block(self) -> str:
        sha = hashlib.sha256()
        sha.update((str(self.timestamp) + str(self.data) + str(self.prev_hash) + str(self.nonce)).encode("utf-8"))
        return sha.hexdigest()

    def sign(self) -> bytes:
        with open('private-key.pem', 'br') as f:
            private_key = RSA.import_key(f.read())
        message = str(self.timestamp) + str(self.data) + str(self.prev_hash) + str(self.hash)
        return base64.b64encode(pkcs1_15.new(private_key).sign(SHA256.new(message.encode())))
    
    def verify(self) -> bool:
        message = str(self.timestamp) + str(self.data) + str(self.prev_hash) + str(self.hash)
        hash = SHA256.new(message.encode())
        try:
            pkcs1_15.new(self.pub_key).verify(hash, base64.b64decode(self.sig))
            return True
        except ValueError:
            return False
