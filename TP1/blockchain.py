# Import required libraries
import time 
import hashlib
import json
from flask import Flask, jsonify, request

# Initialize Flask application
app = Flask(__name__)

# Blockchain class definition
class Blockchain:
    def __init__(self, difficulty=4):
        """Initialize blockchain with genesis block and set difficulty level"""
        self.chain = []  # List to hold blocks
        self.difficulty = difficulty  # Mining difficulty (number of leading zeros required)
        self.create_block(proof=1, previous_hash='0')  # Create genesis block

    def create_block(self, proof, previous_hash):
        """Create new block and add to the chain"""
        block = {
            'index': len(self.chain) + 1,       # Block position in chain
            'timestamp': time.time(),           # Creation timestamp
            'proof': proof,                     # Calculated proof number
            'previous_hash': previous_hash      # Hash of previous block
        }
        self.chain.append(block)
        return block

    def print_previous_block(self):
        """Return last block in the chain"""
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """Mining algorithm to find valid proof that meets difficulty requirements"""
        new_proof = 1  # Start proof search from 1
        valid_proof = False
        
        # Create target string based on current difficulty (e.g., '00000' for difficulty 5)
        target = '0' * self.difficulty
        
        while not valid_proof:
            # Calculate hash using combination of new and previous proofs
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            
            # Check if hash meets difficulty target
            if hash_operation[:self.difficulty] == target:
                valid_proof = True
            else:
                new_proof += 1  # Increment proof if not valid
                
        return new_proof

    def hash(self, block):
        """Generate SHA-256 hash of a block"""
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        """Validate blockchain integrity and proof validity"""
        previous_block = chain[0]  # Start with genesis block
        index = 1
        
        while index < len(chain):
            current_block = chain[index]
            
            # Check if previous_hash matches actual hash of previous block
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
                
            # Verify proof validity
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            hash_operation = hashlib.sha256(
                str(current_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            
            # Check if proof meets difficulty requirements
            if hash_operation[:self.difficulty] != '0' * self.difficulty:
                return False
                
            # Move to next block in chain
            previous_block = current_block
            index += 1
            
        return True  # Return True if all blocks are valid

# Instantiate blockchain with difficulty level 5 (requires 5 leading zeros in hashes)
blockchain = Blockchain(difficulty=5)

# ------------------- FLASK ENDPOINTS ------------------- #

@app.route('/mine_block', methods=['GET'])
def mine_block():
    """Mine new block endpoint"""
    # Get previous block and its proof
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    
    # Find valid proof through proof-of-work
    proof = blockchain.proof_of_work(previous_proof)
    
    # Get hash of previous block
    previous_hash = blockchain.hash(previous_block)
    
    # Create new block and add to chain
    block = blockchain.create_block(proof, previous_hash)
    
    # Build response with block details
    response = {
        'message': 'Congratulations, you mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    
    return jsonify(response), 200  # Return JSON response

@app.route('/get_chain', methods=['GET'])
def display_chain():
    """Display entire blockchain endpoint"""
    response = {
        'chain': blockchain.chain,      # Complete blockchain
        'length': len(blockchain.chain) # Number of blocks
    }
    return jsonify(response), 200

@app.route('/valid', methods=['GET'])
def valid():
    """Blockchain validation endpoint"""
    is_valid = blockchain.chain_valid(blockchain.chain)
    status = 'valid' if is_valid else 'invalid'
    response = {
        'message': f'Blockchain is {status}.'
    }
    return jsonify(response), 200

# Run Flask development server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)