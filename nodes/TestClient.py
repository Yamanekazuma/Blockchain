import datetime as date

from Block import Block
from Blockchain import Blockchain


def next_block(last_block: Block, data: str) -> Block:
    return Block(date.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), data, last_block.hash, last_block.nonce)

def change_block(blockchain: Blockchain) -> None:
    blockchain.chain[int(len(blockchain.chain) / 2)] = Block(date.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "changed data", "0123456789abcdef")

def change_block_data(blockchain: Blockchain) -> None:
    blockchain.chain[int(len(blockchain.chain) / 2)].data = "changed data"

def run() -> None:
    blockchain = Blockchain()
    blocks_num = 20
    for i in range(0, blocks_num):
        new_block = next_block(blockchain.get_last_block(), "index:" + str(i + 1))

        # # ブロック自体の改ざん
        # if (i == 10):
        #     change_block(blockchain)

        # # ブロックデータのみ改ざん
        # if (i == 10):
        #     change_block_data(blockchain)

        if (blockchain.new_block(new_block)):
            print("Tampering with the blockchain was detected.\nThe block was not added to the chain.")
            blockchain.print_chain()
            return
    
    print("Successfully generated blockchain")
    blockchain.print_chain()

if __name__ == "__main__":
    run()
