import json
from common.block import Block
from math import exp,log
import os

simulation = os.path.dirname(__file__)
simulation = simulation.split("common")[0]



def load_blockchain_dag():
    with open(rf"{simulation}common\\blockchain.json", "r") as file_obj:
        blockchain_data = json.load(file_obj)
    return blockchain_data

def store_block(block_to_store: Block):
    blockchain = load_blockchain_dag()
    blockchain[block_to_store.hash] = block_to_store.to_dict
    with open(rf"{simulation}common\\blockchain.json", 'w') as f:
        json.dump(blockchain, f, indent=4)

def get_last_transaction():
    
    blockchain_dag = load_blockchain_dag()
    max_timestamp = float('-inf')
    latest_block_data = None

    for block_hash, block_data in blockchain_dag.items():
        timestamp = block_data['header']['timestamp']
        if timestamp > max_timestamp:
            max_timestamp = timestamp
            latest_block_data = block_data['block']
    return max_timestamp, latest_block_data


def get_user_output(outputs,user):
    for output in outputs:
        if output['locking_script']==user:
            return output['amount']
        else:
            return 0


def get_user_utxo(user):
    user_utxo = 0

    
    blockchain_dag = load_blockchain_dag()

    for block_hash, block in blockchain_dag.items():
            output = get_user_output(block['outputs'],user)
            user_utxo+=output
    return user_utxo

def get_block_amount(block):
    total_amount = 0
    for amounts in block['outputs']:
        total_amount+=amounts['amount']
    return total_amount



def find_block(blockchain,block_hash):
    if block_hash == "0" or block_hash == "1":
        return blockchain["1c7664428394876b6798b51555f68786dbec10203d01d31425f8910b6bfb6956"]   
    return blockchain[block_hash]

def is_valid_block(blockchain_dag,block):
    inputs_sum = 0
    outputs_sum = 0
    parents = block['header']['parentIds']
    if block["hash"] == "1c7664428394876b6798b51555f68786dbec10203d01d31425f8910b6bfb6956" or block["hash"] == "025f5a0ca537b85bf03739ca48279f0445f7d3350851563d30f5c1a501fa76e2":
        return True
    if allUnique(parents):
            for input in block['inputs']:
                inputs_sum+=input['amount']
            for output in block['outputs']:
                outputs_sum+=output['amount']
            if inputs_sum >= outputs_sum:

                for block_hash, existing_block in blockchain_dag.items():
                    if existing_block['header']['timestamp'] < block['header']['timestamp']:
                        if set([_["transaction_hash"] for _ in existing_block["inputs"]]).intersection(set([_["transaction_hash"] for _ in block["inputs"]]))!=set():#Input used only one time
                            return False
                    
            else:
                return False
    else:
        return False
    return True

def allUnique(x):
    seen = list()
    return not any(i in seen or seen.append(i) for i in x)        

def get_block_credit(blockchain_dag,block,alpha,beta):
    sum = 0
    for input in block['inputs']:
        sum +=input['amount']
    if not is_valid_block(blockchain_dag,block):
        return sum*beta*1e-9
    if block['header']['parentIds'] != ['0', '1']:
        parents = [find_block(blockchain_dag,_) for _ in block['header']['parentIds']]
        for parent_block in parents:
            if not is_valid_block(blockchain_dag,parent_block):
                return sum*beta*1e-9
    return sum*alpha*1e-9

def get_user_credit(user,alpha,beta,gamma,start_time,end_time):
    
    blockchain_dag = load_blockchain_dag()
    user_credit = 0
    for block_hash, block in blockchain_dag.items():
        block_timestamp = block['header']['timestamp']
        if end_time > block_timestamp and block['inputs'][0]["unlocking_script"] == user:
            user_credit+=get_block_credit(blockchain_dag,block,alpha,beta)*exp((block_timestamp-end_time))*(1-get_user_proportion(blockchain_dag,user,start_time,block_timestamp))**(gamma)
    return user_credit


def get_total_credit(credits):
    total_credit = 0
    for user,credit in credits.items():
        if credit > 0:
            total_credit+=credit 
    return total_credit

def get_all_credit(alpha,beta,gamma,start_time,end_time):
    blockchain_dag = load_blockchain_dag()
    credit = {}
    for block_hash, block in blockchain_dag.items():
        block_timestamp = block['header']['timestamp']
        user = block['inputs'][0]["unlocking_script"]
        if end_time > block_timestamp:
            if user not in credit:
                credit[user] = 0
            credit[user] += get_block_credit(blockchain_dag,block,alpha,beta)*exp((block_timestamp-end_time))*(1-get_user_proportion(blockchain_dag,user,start_time,block_timestamp))**(gamma)
    return credit

def get_max_credit(credit):
    return credit[max(credit,key=credit.get)]

def get_user_proportion(blockchain_dag,user,start_time,end_time):
    user_number = 0
    total_number = 0
    for block_hash, block in blockchain_dag.items():
        if start_time < block['header']['timestamp'] < end_time:
            total_number+=1
            if block['inputs'][0]['unlocking_script'] == user:
                user_number+=1
    if total_number == 0:
        return 0
    return user_number/total_number

def get_user_timeline():
    blockchain_dag = load_blockchain_dag()
    user_timeline = {}
    with open(rf'{simulation}users.json', "r") as file_obj:
        users = json.load(file_obj)
   
    for user in users.keys():
        user_timeline.update({users[user]['public_key_hash']:{'valid_transaction':[],'invalid_transaction':[]}})
    for block_hash, block in blockchain_dag.items():
        if is_valid_block(blockchain_dag,block):
            user_timeline[block['inputs'][0]['unlocking_script']]['valid_transaction'].append(block['block'])
        else:
            user_timeline[block['inputs'][0]['unlocking_script']]['invalid_transaction'].append(block['block'])
    with open(rf"{simulation}user_timeline.json", "w") as file:
        json.dump(user_timeline, file)



def validate_all_blocks():
    blockchain_dag = load_blockchain_dag()
    transaction_validity = {'valid_transaction':{},'invalid_transaction':{}}
    
    
    for block_hash, block in blockchain_dag.items():
        if is_valid_block(block):
            transaction_validity['valid_transaction'][block_hash] = block
        else:
            transaction_validity['invalid_transaction'][block_hash] = block
    with open(rf"{simulation}transaction_validity.json", "w") as file:
        json.dump(transaction_validity, file)






