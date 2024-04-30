import json
from time import time
from common.wallet import Owner
import os

simulation = os.path.dirname(__file__)
simulation = simulation.split("simulation")[0]
def generate_random_user(number=2):

    with open(rf"{simulation}simulation\\users.json" , "r") as f:
        with open(rf"{simulation}common\\user_credit.json" , "r") as g:
            file_credit = json.load(g)
            file_user = json.load(f)
            for i in range(number):
                user = Owner()
                file_user[f"user{i+2}"]={"private_key": user.private_key.export_key("DER").decode('ISO-8859-1')  ,"public_key_hex": user.public_key_hex,"public_key_hash": user.public_key_hash}
                file_credit[user.public_key_hash]=(1,time())
    with open(rf"{simulation}simulation\\users.json" , "w") as f:
        f.write(json.dumps(file_user,indent=i))
    with open(rf"{simulation}common\\user_credit.json" , "w") as g:
        g.write(json.dumps(file_credit,indent=i))