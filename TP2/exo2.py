import hashlib

def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_merkle_tree(transactions):
    """Builds a Merkle tree and returns the root and the tree structure."""
    tree = []
    leaves = [sha256(tx) for tx in transactions]
    tree.append(leaves)

    while len(leaves) > 1:
        if len(leaves) % 2 == 1:  
            leaves.append(leaves[-1])

        new_level = []
        for i in range(0, len(leaves), 2):
            new_level.append(sha256(leaves[i] + leaves[i + 1]))
        leaves = new_level
        tree.append(leaves)

    return tree[-1][0], tree  

def merkle_proof(transactions, target_tx):
    """Generate a Merkle proof for the given target transaction."""
    proof = []
    _, tree = build_merkle_tree(transactions)

    leaves = tree[0]  
    target_hash = sha256(target_tx)
    
    if target_hash not in leaves:
        return None  

    index = leaves.index(target_hash)  

    for level in tree[:-1]:  
        if index % 2 == 0:  
            sibling_index = index + 1 if index + 1 < len(level) else index
        else:  
            sibling_index = index - 1

        proof.append((level[sibling_index], index % 2 == 0))  
        index = index // 2  

    return proof

def verify_merkle_proof(proof, target_tx, root):
    """Verify a Merkle proof for the given target transaction."""
    target_hash = sha256(target_tx)

    for sibling_hash, is_left in proof:
        if is_left:
            target_hash = sha256(target_hash + sibling_hash)
        else:
            target_hash = sha256(sibling_hash + target_hash)

    return target_hash == root  


transactions = ["tx1", "tx2", "tx3", "tx4"]
root, _ = build_merkle_tree(transactions)


proof = merkle_proof(transactions, "tx3")

print(f"Merkle Root: {root}")
print(f"Merkle Proof for 'tx3': {proof}")

# Verify the proof for "tx3"
is_valid = verify_merkle_proof(proof, "tx3", root)
print(f"Verification Result: {is_valid}")