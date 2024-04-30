import networkx as nx
from pyvis.network import Network
import json
from common.utils import is_valid_block,find_block,get_block_credit,get_user_credit,load_blockchain_dag
import time

def DrawBlockchain():
    nt = Network(notebook=True, directed=True)
    nt.options = { "layout": { "hierarchical": { "enabled": True,
        "direction": "RL",
        "sortMethod": "directed",
        "levelSeparation": 200} } ,
    }

    blockchain = load_blockchain_dag()
    G = nx.DiGraph()
    for block_hash, block in blockchain.items():
        G.add_node(block_hash)
        for parent in block['header']['parentIds']:
            G.add_edge(block_hash,parent)
        if is_valid_block(blockchain,block):
            G.nodes[block_hash]['color'] = "green"
            for parent in block['header']['parentIds']:
                if not is_valid_block(blockchain,find_block(blockchain,parent)):
                    G.nodes[block_hash]['color'] = "red"
        else:
            G.nodes[block_hash]['color'] = "red"
    
    nt.from_nx(G)
    nt.show("network.html")

