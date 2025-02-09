import time 
import hashlib
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def print_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        valid_proof = False
        
        target = '0' * self.difficulty
        
        while not valid_proof:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            
            if hash_operation[:self.difficulty] == target:
                valid_proof = True
            else:
                new_proof += 1
                
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        index = 1
        
        while index < len(chain):
            current_block = chain[index]
            
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
                
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            hash_operation = hashlib.sha256(
                str(current_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            
            if hash_operation[:self.difficulty] != '0' * self.difficulty:
                return False
                
            previous_block = current_block
            index += 1
            
        return True

blockchain = Blockchain(difficulty=5)

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    
    response = {
        'message': 'Congratulations, you mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/valid', methods=['GET'])
def valid():
    is_valid = blockchain.chain_valid(blockchain.chain)
    response = {
        'message': 'Blockchain is valid.' if is_valid else 'Blockchain is invalid!'
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)