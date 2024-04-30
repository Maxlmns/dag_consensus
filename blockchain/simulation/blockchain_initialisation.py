from datetime import datetime
import json
from common.block import Block, BlockHeader
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from common.wallet import Owner
from common.utils import store_block
import os
simulation = os.path.dirname(__file__)
simulation = simulation.split("simulation")[0]
def initialize_blockchain():
    with open(rf"{simulation}common\\blockchain.json", "w") as f:
        f.write(json.dumps({}))          
    with open(rf"{simulation}simulation\\users.json" , "r") as f:
            users = json.load(f)
    
    user0 = Owner(users["user0"]['private_key'].encode('ISO-8859-1'))
    user1 = Owner(users["user1"]['private_key'].encode('ISO-8859-1'))

    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2024-01-01 00:00:00.000'))
    input_0 = TransactionInput(user0, timestamp_0, transaction_hash="transaction0", amount=5e+8)
    output_0 = TransactionOutput(user0.public_key_hash, input_0.hash , amount=5e+8)
    block_header_0 = BlockHeader(parentIds=["0", "1"], timestamp=timestamp_0, noonce=1)
    block_0 = Block(inputs=[input_0.to_dict()], outputs=[output_0.to_dict()], block_header=block_header_0)

    timestamp_1 = datetime.timestamp(datetime.fromisoformat('2024-01-01 00:00:00.000'))
    input_1 = TransactionInput(user1, timestamp_1, transaction_hash="transaction1", amount=5e+8)
    output_1 = TransactionOutput(user1.public_key_hash,input_1.hash ,amount=5e+8)
    block_header_1 = BlockHeader(parentIds=["0", "1"], timestamp=timestamp_1, noonce=2)
    block_1 = Block(inputs=[input_1.to_dict()], outputs=[output_1.to_dict()], block_header=block_header_1)
   
    store_block(block_0)   
    store_block(block_1)
