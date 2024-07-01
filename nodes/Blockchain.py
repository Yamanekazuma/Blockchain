import datetime as date
import requests
from urllib.parse import urlparse
import base64

from Block import Block

URL = "127.0.0.1"


class Blockchain():
    def __init__(self, chain: list[Block] = None) -> None:
        self.nodes: set[str] = set()
        if (chain is None):
            self.chain = [self.__create_genesis_block("genesis block")]
        else:
            self.chain = chain

    def register_node(self, address: str) -> None:
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # 追加できない場合は1を返す
    def new_block(self, block: Block) -> int:
        if (self.verify_blockchain() == 0):
            self.chain.append(block)
            return 0
        else:
            return 1

    def get_last_block(self) -> Block:
        return self.chain[-1]

    @staticmethod
    def __create_genesis_block(data: str) -> Block:
        return Block(date.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), data, "0", 0)

    # 正しい場合0を、不正な場合1を返す
    def verify_blockchain(self) -> int:
        if (self.chain == []):
            return 0

        prev_block_hash = self.chain[0].hash
        prev_block_nonce = self.chain[0].nonce
        for block in self.chain[1:]:
            # 直前ハッシュの一致 + 署名による改ざん検知 + PoWによるコンセンサスアルゴリズムの確認
            if (block.prev_hash != prev_block_hash or not block.verify() or not block.is_valid_proof(prev_block_nonce, block.nonce)):
                return 1
            prev_block_hash = block.hash
            prev_block_nonce = block.nonce
        return 0

    def print_chain(self, start_index: int = -1, end_index: int = -1) -> None:
        if (start_index == -1):
            start_index = 0
        if (end_index == -1):
            end_index = len(self.chain)

        prev_data = self.chain[start_index].data
        prev_prev_hash = self.chain[start_index].prev_hash
        prev_hash = self.chain[start_index].hash
        if (start_index + 1 > end_index):
            print(f"Data: {prev_data}")
            print(f"PrevHash: {prev_prev_hash}")
            print(f"Hash: {prev_hash}\n")
            return

        for block in self.chain[start_index + 1: end_index + 2]:
            if (block.prev_hash != prev_hash):
                print(f"Data: {prev_data}")
                print(f"PrevHash: {prev_prev_hash}")
                print("Hash: {}\n".format('\033[31m' + prev_hash + '\033[0m'))
                prev_prev_hash = '\033[31m' + prev_hash + '\033[0m'
            else:
                print(f"Data: {prev_data}")
                print(f"PrevHash: {prev_prev_hash}")
                print(f"Hash: {prev_hash}")
                prev_prev_hash = block.prev_hash

            prev_data = block.data
            prev_hash = block.hash

    def resolve_conflicts(self) -> bool:
        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbors:
            headers = {"Referer": URL}
            response = requests.get(f"http://{node}/chain", headers=headers)
            if (response.status_code == 200):
                length = int(response.json()["length"])
                chain = response.json()["chain"]

                if (length > max_length):
                    blocks = []
                    for block in chain:
                        blocks.append(Block(block["timestamp"], block["data"], block["prev_hash"], nonce=int(
                            block["nonce"]), hash=block["hash"], sig=base64.b64decode(block["sig"]), pub_key=base64.b64decode(block["pub_key"])))
                    if (Blockchain(chain=blocks).verify_blockchain() == 0):
                        max_length = length
                        new_chain = blocks

        if (not new_chain is None):
            self.chain = new_chain
            return True
