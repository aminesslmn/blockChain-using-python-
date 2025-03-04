import hashlib
import datetime

# Helper function to compute SHA-256 hash
def sha256(data):
    """Returns the SHA-256 hash of the given data."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Function to build a Merkle tree and return the root
def build_merkle_tree(transactions):
    """Builds a Merkle tree and returns the root."""
    if not transactions:
        return sha256("")  # Empty tree hash
    
    # Hash all transactions to create the leaves
    leaves = [sha256(tx) for tx in transactions]
    
    # Build the tree level by level
    while len(leaves) > 1:
        if len(leaves) % 2 == 1:  # If odd, duplicate the last leaf
            leaves.append(leaves[-1])
        new_level = []
        for i in range(0, len(leaves), 2):
            combined = leaves[i] + leaves[i + 1]
            new_level.append(sha256(combined))
        leaves = new_level
    
    return leaves[0]  # The Merkle root

# Block class
class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = build_merkle_tree(transactions)  # Compute Merkle root
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Generate the block's hash."""
        block_string = str(self.index) + str(self.timestamp) + self.merkle_root + self.previous_hash
        return sha256(block_string)

# Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """Create the first block in the blockchain (genesis block)."""
        return Block(0, str(datetime.datetime.now()), ["Genesis Block"], "0")

    def add_block(self, transactions):
        """Add a new block to the blockchain."""
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), str(datetime.datetime.now()), transactions, last_block.hash)
        self.chain.append(new_block)

# Function to verify a block's Merkle root
def verify_block(block):
    """Verifies that the block's Merkle root matches the transactions."""
    computed_merkle_root = build_merkle_tree(block.transactions)
    return computed_merkle_root == block.merkle_root

# Example usage
if __name__ == "__main__":
    # Create a blockchain
    blockchain = Blockchain()

    # Add blocks with transactions
    blockchain.add_block(["tx1", "tx2", "tx3"])
    blockchain.add_block(["tx4", "tx5"])

    # Print blockchain details
    for block in blockchain.chain:
        print(f"Block #{block.index}:")
        print(f"Hash: {block.hash}")
        print(f"Merkle Root: {block.merkle_root}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Transactions: {block.transactions}")
        print()

    # Verify the blockchain
    print("Verifying blockchain integrity:")
    for block in blockchain.chain:
        if verify_block(block):
            print(f"Block #{block.index} is valid.")
        else:
            print(f"Block #{block.index} is invalid.")