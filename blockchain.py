#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json
import datetime
import hashlib  # for SHA-256

import ecdsa  # Elliptic Curve Digital Signature Algorithm


class Blockchain:
    def __init__(self, genesis_block_data=None):
        """
        Initialize the blockchain with the genesis block.

        :param genesis_block_data: Data to be put in the genesis (first) block of the blockchain.
        """
        self.blocks = []  # initialize the list of blocks
        self.mine_block(genesis_block_data)  # add the genesis block

    @staticmethod
    def hash_block(block):
        """
        Encode the block to JSON and hashes it.


        :param block: The block to hash.
        :return: Hexadecimal string representation of SHA-256 hash of the block encoded in JSON.
        """
        # sort_keys=True is important for consistent results of JSON encoding:
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()  # Secure Hash Algorithm

    def mine_block(self, block_data):
        """
        Mine a new block to the end of the blockchain.

        :param block_data: The data to be stored in the new block.
        """

        block = {}

        block['index'] = len(self.blocks)  # set the next consecutive block index
        block['timestamp'] = str(datetime.datetime.now())  # store the current date and time
        block['data'] = block_data  # user data to be stored in the block
        # set the previous hash if there are blocks in the blockchain or the default value otherwise:
        block['previous_hash'] = self.hash_block(self.blocks[-1]) if len(self.blocks) else 'none'

        # calculate the proof of work:
        block['nonce'] = 0  # initialize the nonce
        while self.hash_block(block)[:3] != '000':  # check that last 3 digits of the hash are zeroes
            block['nonce'] += 1  # repeat until a required hash has been found

        self.blocks.append(block)  # add the block to the chain

    def validate(self, start_block_index=1):
        """
        Check the validity of the blockchain. Validate hashes and proofs of work in the blockchain.

        :param start_block_index: Block index to start validation from.
        :return: True if the blockchain is valid.
        """

        for block_index in range(start_block_index, len(self.blocks)):  # loop through all the required blocks
            block = self.blocks[block_index]
            # hash the previous block and compare the hash with the hash stored in the current block:
            if block['previous_hash'] != self.hash_block(self.blocks[block_index - 1]):
                return False
            if self.hash_block(block)[:3] != '000':  # check the nonce
                return False
        return True


class Wallet:
    def __init__(self):
        """
        Initialize the wallet with private key and public key using ECDSA.
        """

        self.private_key = ecdsa.SigningKey.generate()  # generate a random ECDSA private key (signing key)
        self.public_key = self.private_key.get_verifying_key()  # derive the public key from the private key

    def get_private_key(self):
        """
        Encode the private key to Base64.

        :return: Private key encoded in Base64.
        """

        return base64.b64encode(self.private_key.to_string()).decode()

    def get_public_key(self):
        """
        Encode the public key to Base64.

        :return: Public key encoded in Base64.
        """

        return base64.b64encode(self.public_key.to_string()).decode()


class Cryptocurrency:
    def __init__(self):
        """
        Initialize the blockchain and the list of transactions.
        """

        self.blockchain = Blockchain({'transactions': []})  # genesis block contains an empty list of transactions
        self.transactions = []

    def add_transaction(self, wallet, to, amount):
        """
        Add a new transaction to the list of current transactions.

        :param wallet: The wallet to send the coins from.
        :param to: The address to send the coins to.
        :param amount: Amount of coins.
        """
        transaction = {}

        transaction['data'] = {}  # 'data' is used to split the transaction data from its signature
        transaction['data']['from'] = wallet.get_public_key()  # use the waller's public key as the sender's address
        transaction['data']['to'] = to
        transaction['data']['amount'] = amount

        # encode the transaction data to JSON:
        transaction_data = json.dumps(transaction['data'], sort_keys=True).encode()
        # sign the transaction data using the waller's private key:
        transaction['signature'] = base64.b64encode(wallet.private_key.sign(transaction_data)).decode()

        self.transactions.append(transaction)  # add the transaction to the list

    def mine_block(self, reward_address):
        """
        Mine the next block of current transactions.

        :param reward_address: the reward address for the coinbase transaction.
        """

        # add the reward (coinbase) transaction to the list of current transactions:
        self.transactions.append(
            {'data': {'from': 'network', 'to': reward_address, 'amount': 10}, 'signature': 'reward'})
        # mine the next block and include it in the blockchain:
        self.blockchain.mine_block({'transactions': self.transactions})
        self.transactions = []  # clear out the transaction list

    def validate_blockchain(self, start_block_index=1):
        """
        Check the validity of the blockchain. Validate hashes and signatures of transactions in the blockchain.

        :param start_block_index: Block index to start validation from.
        :return: True if the blockchain is valid.
        """

        if not self.blockchain.validate(start_block_index):  # validate block hashes
            return False

        for block_index in range(start_block_index,
                                 len(self.blockchain.blocks)):  # loop through all the required blocks
            block = self.blockchain.blocks[block_index]
            for transaction in block['data']['transactions']:  # loop through all transactions
                if transaction['data']['from'] == 'network':  # if it's a coinbase transaction then ignore it
                    continue

                # get the public key from the transaction:
                public_key = ecdsa.VerifyingKey.from_string(base64.b64decode(transaction['data']['from']))
                # get the signature from the transaction:
                signature = base64.b64decode(transaction['signature'])
                # encode transaction data to JSON:
                transaction_data = json.dumps(transaction['data'], sort_keys=True).encode()
                # check the transaction signature with the public key:
                if not public_key.verify(signature, transaction_data):
                    return False

        return True

    def calculate_balance(self, address):
        """
        Calculate the balance of the given address.
        :param address: Address to calculate the balance.
        :return: Balance of the given address.
        """
        balance = 0
        for block in self.blockchain.blocks:  # loop through all blocks
            for transaction in block['data']['transactions']:  # loop through all transactions
                # if it's an outgoing transaction then subtract the specified amount from the balance:
                if transaction['data']['from'] == address:
                    balance -= transaction['data']['amount']
                # if it's an incoming transaction then add the specified amount to the balance:
                if transaction['data']['to'] == address:
                    balance += transaction['data']['amount']

        return balance


class Application:
    def run(self):
        """
        Create source and target wallets, mine a block to emit initial coins, make 2 transactions to send coins from the
        source wallet to the target wallet, mine a block to include the current transactions.
        """

        source_wallet = Wallet()  # create the wallet
        # print wallet's private and public keys:
        print('source wallet:')
        print('  private key: {}'.format(source_wallet.get_private_key()))
        print('  public  key: {}'.format(source_wallet.get_public_key()))
        print()

        target_wallet = Wallet()  # create the wallet
        # print wallet's private and public keys:
        print('target wallet:')
        print('  private key: {}'.format(target_wallet.get_private_key()))
        print('  public  key: {}'.format(target_wallet.get_public_key()))
        print()

        cryptocurrency = Cryptocurrency()
        cryptocurrency.mine_block(source_wallet.get_public_key())  # mine a block to emit initial coins
        # make 2 transactions to send coins from the source wallet to the target wallet:
        cryptocurrency.add_transaction(source_wallet, target_wallet.get_public_key(), 2.5)
        cryptocurrency.add_transaction(source_wallet, target_wallet.get_public_key(), 3.5)
        # mine a block to include the current transactions:
        cryptocurrency.mine_block(source_wallet.get_public_key())

        # check the validity of the blockchain:
        if cryptocurrency.validate_blockchain():
            print('blockchain is valid')
        print()

        # print all blocks and transactions:
        print('blockchain:')
        print('{: <5} {: <26} {}'.format('index', 'timestamp', 'previous_hash'))
        for block in cryptocurrency.blockchain.blocks:
            # format and print block data:
            print('{: <5} {} {: <64}'.format(block['index'], block['timestamp'], block['previous_hash']))

            # format and print transaction data:
            if len(block['data']['transactions']):
                print('  transactions:')
                print('  {: <64} {: <64} {: <6} {}'.format('from', 'to', 'amount', 'signature'))
            for transaction in block['data']['transactions']:
                transaction_data = transaction['data']
                print('  {: <64} {} {: <6} {}'.format(transaction_data['from'], transaction_data['to'],
                                                      transaction_data['amount'], transaction['signature']))
        print()

        # print wallet balances:
        print('source wallet:')
        print('  balance: {}'.format(cryptocurrency.calculate_balance(source_wallet.get_public_key())))
        print('target wallet:')
        print('  balance: {}'.format(cryptocurrency.calculate_balance(target_wallet.get_public_key())))


if __name__ == '__main__':
    Application().run()  # run the application's instance
