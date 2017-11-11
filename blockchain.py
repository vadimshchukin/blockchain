import base64
import json
import datetime
import hashlib

import ecdsa


class Blockchain:
    def __init__(self, genesis_block_data=None):
        self.blocks = [] # initialize the list of blocks
        self.add_block(genesis_block_data) # add the genesis block

    @staticmethod
    def hash_block(block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def add_block(self, block_data):
        block = {}

        block['index'] = len(self.blocks)
        block['timestamp'] = str(datetime.datetime.now())
        block['data'] = block_data
        block['previous_hash'] = self.hash_block(self.blocks[-1]) if len(self.blocks) else 'none'

        # calculate the proof of work:
        block['nonce'] = 0
        while self.hash_block(block)[:3] != '000':
            block['nonce'] += 1

        self.blocks.append(block)

    def validate(self, start_block_index=1):
        for block_index in range(start_block_index, len(self.blocks)):
            block = self.blocks[block_index]
            if block['previous_hash'] != self.hash_block(self.blocks[block_index - 1]):
                return False
        return True

class Cryptocurrency:
    def __init__(self):
        self.blockchain = Blockchain({'transactions': []})
        self.transactions = []

    def add_transaction(self, wallet, to, amount):
        transaction = {}

        transaction['data'] = {}
        transaction['data']['from'] = wallet.get_public_key()
        transaction['data']['to'] = to
        transaction['data']['amount'] = amount

        transaction_data = json.dumps(transaction['data'], sort_keys=True).encode()
        transaction['signature'] = base64.b64encode(wallet.private_key.sign(transaction_data)).decode()

        self.transactions.append(transaction)

    def add_block(self, reward_address):
        self.transactions.append({'data': {'from': 'network', 'to': reward_address, 'amount': 10}, 'signature': 'reward'})
        self.blockchain.add_block({'transactions': self.transactions})
        self.transactions = []

    def validate_blockchain(self, start_block_index=1):
        if not self.blockchain.validate(start_block_index):
            return False
        for block_index in range(start_block_index, len(self.blockchain.blocks)):
            block = self.blockchain.blocks[block_index]
            for transaction in block['data']['transactions']:
                if transaction['data']['from'] == 'network':
                    continue
                public_key = ecdsa.VerifyingKey.from_string(base64.b64decode(transaction['data']['from']))
                signature = base64.b64decode(transaction['signature'])
                transaction_data = json.dumps(transaction['data'], sort_keys=True).encode()
                if not public_key.verify(signature, transaction_data):
                    return False
        return True

    def calculate_balance(self, address):
        balance = 0
        for block in self.blockchain.blocks:
            for transaction in block['data']['transactions']:
                if transaction['data']['from'] == address:
                    balance -= transaction['data']['amount']
                if transaction['data']['to'] == address:
                    balance += transaction['data']['amount']
        return balance


class Wallet:
    def __init__(self):
        self.private_key = ecdsa.SigningKey.generate()
        self.public_key = self.private_key.get_verifying_key()

    def get_private_key(self):
        return base64.b64encode(self.private_key.to_string()).decode()

    def get_public_key(self):
        return base64.b64encode(self.public_key.to_string()).decode()


source_wallet = Wallet()
print('source wallet:')
print('  public  key: {}'.format(source_wallet.get_private_key()))
print('  private key: {}'.format(source_wallet.get_public_key()))
print()

target_wallet = Wallet()
print('target wallet:')
print('  public  key: {}'.format(target_wallet.get_private_key()))
print('  private key: {}'.format(target_wallet.get_public_key()))
print()

cryptocurrency = Cryptocurrency()
cryptocurrency.add_block(source_wallet.get_public_key())
cryptocurrency.add_transaction(source_wallet, target_wallet.get_public_key(), 2.5)
cryptocurrency.add_transaction(source_wallet, target_wallet.get_public_key(), 3.5)
cryptocurrency.add_block(source_wallet.get_public_key())
if cryptocurrency.validate_blockchain():
    print('blockchain is valid')
print()

print('blockchain:')
print('{: <5} {: <26} {}'.format('index', 'timestamp', 'previous_hash'))
for block in cryptocurrency.blockchain.blocks:
    print('{: <5} {} {: <64}'.format(block['index'], block['timestamp'], block['previous_hash']))
    if len(block['data']['transactions']):
        print('  transactions:')
        print('  {: <64} {: <64} {: <6} {}'.format('from', 'to', 'amount', 'signature'))
    for transaction in block['data']['transactions']:
        transaction_data = transaction['data']
        print('  {: <64} {} {: <6} {}'.format(transaction_data['from'], transaction_data['to'], transaction_data['amount'], transaction['signature']))
print()

print('source wallet:')
print('  balance: {}'.format(cryptocurrency.calculate_balance(source_wallet.get_public_key())))
print('target wallet:')
print('  balance: {}'.format(cryptocurrency.calculate_balance(target_wallet.get_public_key())))