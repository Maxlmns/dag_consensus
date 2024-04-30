import json
from time import time

USER_REPUTATION_FILENAME = "common/user_credit.json"


def load_user_reputations():
    try:
        with open(USER_REPUTATION_FILENAME, 'r') as file:
            user_reputations = json.load(file)
    except FileNotFoundError:
        user_reputations = {}
    return user_reputations

def save_user_reputations(public_key,reputation):

    try:
        with open(USER_REPUTATION_FILENAME, "r") as file_obj:
            existing_data = json.load(file_obj)
    except (json.JSONDecodeError, FileNotFoundError):
        existing_data = []
    

    for  k in range(len(existing_data)):
        if public_key in existing_data[k]:
            existing_data.pop(k)
            break
    existing_data.append({public_key:[reputation,time()]})

    with open(USER_REPUTATION_FILENAME, "w") as file_obj:
            json.dump(existing_data, file_obj)

