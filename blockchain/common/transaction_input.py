import json
from common.wallet import Owner
from common.wallet import calculate_hash
class TransactionInput:
    def __init__(self,user,timestamp,transaction_hash, amount):
        self.unlocking_script = user.public_key_hash
        self.transaction_hash = transaction_hash
        self.amount = amount
        self.timestamp = timestamp
        self.hash = self.get_hash()

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self):
            return {
                "unlocking_script":self.unlocking_script,
                "transaction_hash": self.transaction_hash,
                "amount": self.amount,
                "timestamp": self.timestamp
            }
    def get_hash(self) -> str:
        data = {
            "unlocking_script": self.unlocking_script,
            "transaction_hash": self.transaction_hash,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
        return calculate_hash(json.dumps(data))