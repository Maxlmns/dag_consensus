import json
from common.wallet import calculate_hash


class TransactionOutput:
    def __init__(self, public_key_hash,input_hash, amount):
        self.amount = amount
        self.locking_script = public_key_hash
        self.input_hash = input_hash
        self.hash = self.get_hash()

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "locking_script": self.locking_script,
            "input_hash": self.input_hash,
            "hash": self.hash,

        }
    def get_hash(self) -> str:
        data = {
            "amount": self.amount,
            "input_hash": self.input_hash,
            "locking_script": self.locking_script,
        }
        return calculate_hash(json.dumps(data))
