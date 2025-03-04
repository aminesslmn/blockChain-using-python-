import hashlib

def sha256(data):
    """Returns the SHA-256 hash of the given data."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_merkle_tree(transactions):
    """Builds the Merkle tree and returns the Merkle root."""
    leaves = [sha256(tx) for tx in transactions]
    while len(leaves) > 1:
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1])  
        leaves = [sha256(leaves[i] + leaves[i+1]) for i in range(0, len(leaves), 2)]
    return leaves[0]  
transactions = ["tx1", "tx2", "tx3", "tx4"]
root = build_merkle_tree(transactions)
print(f"Merkle Root: {root}")
