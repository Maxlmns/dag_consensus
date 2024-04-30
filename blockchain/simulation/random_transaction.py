from datetime import datetime
import json
from common.block import Block, BlockHeader
from common.utils import load_blockchain_dag,is_valid_block,find_block,store_block
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from random import randint,choice
from common.wallet import Owner
from hashlib import sha256
import os

simulation = os.path.dirname(__file__)
simulation = simulation.split("simulation")[0]

def generate_random_transaction(numberTransactions):
    
    try:
        with open(rf"{simulation}simulation\\users.json" , "r") as f:
            users = json.load(f)
    except Exception as e:
        print(e)
        users = {}

    amount_i = randint(1, 500000000)
    user = Owner(users["user0"]['private_key'].encode('ISO-8859-1'))
    last_malicious1 = "1c7664428394876b6798b51555f68786dbec10203d01d31425f8910b6bfb6956"
    last_malicious2 = "1c7664428394876b6798b51555f68786dbec10203d01d31425f8910b6bfb6956"
    number_users = len(users)
    input_hash = "3fd79beffc66b7fd9c62623495bbac4dd71ecb73eb25a51f2ce2003a0ad48ab5"
    for number in range(numberTransactions):
        timestamp = datetime.now().timestamp()
        blockchain = load_blockchain_dag()

        amount_i = randint(1, amount_i)
        
        random_user = randint(0, number_users-1)
        
        output_hash = user.public_key_hash

        if random_user<number_users/3:
            malicious_user = Owner(users[f"user{random_user}"]['private_key'].encode('ISO-8859-1'))
            malicious_input =  "3924170d934b84af68953335258674675d77bffcfc4e48d78993bfb9f7f50303"
            input = TransactionInput(malicious_user, timestamp, transaction_hash= malicious_input, amount=amount_i)
            output = TransactionOutput(output_hash,malicious_input, amount_i+1)

            random_parent1 = last_malicious1
            random_parent2 = last_malicious2

        

        else:
            random_parent1 = choice(list(blockchain.keys()))
            random_parent2 = choice(list(blockchain.keys()))
            while not is_valid_block(blockchain,find_block(blockchain,random_parent1)):
                    random_parent1 = choice(list(blockchain.keys()))
            while not is_valid_block(blockchain,find_block(blockchain,random_parent2)) or random_parent1==random_parent2:
                    random_parent2 = choice(list(blockchain.keys()))
            input = TransactionInput(user, timestamp, transaction_hash=input_hash, amount=amount_i)

            output = TransactionOutput(output_hash, input.hash ,amount_i)
            input_hash = output.hash
        
            user = Owner(users[f"user{random_user}"]['private_key'].encode('ISO-8859-1'))

        random_parents = [random_parent1, random_parent2]
        
        block_header = BlockHeader(parentIds=random_parents, timestamp=timestamp, noonce=2)
        
        block_to_store = Block(inputs=[input.to_dict()], outputs=[output.to_dict()], block_header=block_header)
        
        store_block(block_to_store)

        if random_user<number_users/3:
             last_malicious1 = last_malicious2
             last_malicious2 = block_to_store.hash

        