import json

from common.wallet import calculate_hash

class BlockHeader:
    def __init__(self,parentIds, timestamp, noonce  ):
        self.parentIds = parentIds
        self.timestamp = timestamp
        self.noonce = noonce

    def __eq__(self, other):
        try:
            assert self.parentIds == other.parentIds
            assert self.timestamp == other.timestamp
            assert self.noonce == other.noonce
            return True
        except AssertionError:
            return False

    

    @property
    def to_dict(self) -> dict:
        return {
            "parentIds": self.parentIds,
            "timestamp": self.timestamp,
            "noonce": self.noonce,
        }

    def __str__(self):
        return json.dumps(self.to_dict)

    @property
    def to_json(self) -> str:
        return json.dumps(self.to_dict)


class Block:
    def __init__(
        self, block_header, inputs, outputs
    ):
        self.block_header = block_header
        self.inputs = inputs
        self.outputs = outputs
        self.hash = self.get_hash()

    def get_hash(self) -> str:
        data = {
            "block_header": self.block_header.to_dict,
            "inputs": self.inputs,
            "outputs": self.outputs,
        }
        return calculate_hash(json.dumps(data))
    def __eq__(self, other):
        try:
            assert self.block_header == other.block_header
            assert self.inputs == other.inputs
            assert self.outputs == other.outputs
                        
            assert self.hash == other.hash

            return True
        except AssertionError:
            return False
        
    def __str__(self):
        return json.dumps(self.to_dict)
                        

    @property
    def to_dict(self):
        return {
            "header": self.block_header.to_dict,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "hash": self.hash
        }

    @property
    def to_json(self) -> str:
        return json.dumps(self.to_dict)


    