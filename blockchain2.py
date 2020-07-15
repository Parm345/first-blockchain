import hashlib
import json
from time import time

class Blockchain(object):
    
    def __init__(self):
        self.chain = []
        self.current_transaction = []

        self.new_block(100, og_hash = '1')

    def new_transaction(self, sender, recipient, amount):
        
        # adds the current transaction
        self.current_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

    def new_block(self, proof, og_hash = None):
        
        block = {
            'index': len(self.chain) + 1,
            'time': time(),
            'transaction': self.current_transaction,
            'proof': proof,
            'previous_hash': og_hash or self.hash(self.chain[-1])
        }

        self.chain.append(block)

        self.current_transaction = []

    def last_block(self):
        return self.chain[-1]

    def hash(self, _block):
        block = json.dumps(_block, sort_keys=True).encode()
        return hashlib.sha256(block).hexdigest()

    def proof_of_work(self, last_proof):
        
        proof = 0

        while self.find_proof(last_proof, proof) == False:
           proof += 1

        return proof

    def find_proof(self, last_proof, proof):
        
        guess = f'{last_proof}{proof}'.encode()
        hashed_guess = hashlib.sha256(guess).hexdigest()
        return hashed_guess[:1] == '0'


blockchain = Blockchain()

def mine():
    last_block = blockchain.last_block()
    last_proof = last_block['proof']

    return blockchain.proof_of_work(last_proof)

def transaction():
    sender = input('Sender: ')
    recipient = input('Recipient: ')
    amount = input('Amount: ')

    blockchain.new_transaction(sender, recipient, amount)
    blockchain.new_block(mine())

run = True

while run:
    response = input('What would you like to do?: ')

    if response == 'e':
        run = False
    elif response == 't':
        transaction()
        print(blockchain.chain)
    else:
        print('Invalid input, try again')

#blockchain.new_transaction('TJ', 'Franklin', '10')
#blockchain.new_block(100)
#print(blockchain.chain)
#mine()