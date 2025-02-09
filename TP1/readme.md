# Blockchain Implementation with Flask

## Overview
This project is a simple blockchain implementation using Python and Flask. It includes essential blockchain functionalities such as block creation, proof-of-work mining, and chain validation, accessible via a REST API.

## Features
- **Genesis Block**: Automatically creates the first block in the blockchain.
- **Proof-of-Work (PoW)**: Implements a mining algorithm requiring a specified difficulty level.
- **Block Hashing**: Uses SHA-256 to hash block data.
- **Blockchain Integrity Validation**: Ensures the chain's validity by checking hashes and proof values.
- **Flask API Endpoints**:
  - `/mine_block` - Mines a new block and adds it to the blockchain.
  - `/get_chain` - Retrieves the full blockchain.
  - `/valid` - Checks if the blockchain is valid.

## Installation
### Prerequisites
- Python 3.x
- Flask

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/blockchain-flask.git
   cd blockchain-flask
   ```
2. Install dependencies:
   ```sh
   pip install flask
   ```
3. Run the application:
   ```sh
   python app.py
   ```
4. The server will start at `http://127.0.0.1:5000/`

## API Endpoints
### 1. Mine a New Block
- **Endpoint**: `GET /mine_block`
- **Description**: Mines a new block and adds it to the blockchain.
- **Response Example**:
  ```json
  {
      "message": "Congratulations, you mined a block!",
      "index": 2,
      "timestamp": 1699202603.482,
      "proof": 35293,
      "previous_hash": "00000a3bc4..."
  }
  ```

### 2. Get the Blockchain
- **Endpoint**: `GET /get_chain`
- **Description**: Retrieves the entire blockchain.
- **Response Example**:
  ```json
  {
      "chain": [
          { "index": 1, "timestamp": 1699202603.482, "proof": 1, "previous_hash": "0" },
          { "index": 2, "timestamp": 1699202901.123, "proof": 35293, "previous_hash": "00000a3bc4..." }
      ],
      "length": 2
  }
  ```

### 3. Validate Blockchain
- **Endpoint**: `GET /valid`
- **Description**: Checks if the blockchain is valid.
- **Response Example**:
  ```json
  { "message": "Blockchain is valid." }
  ```

## How the Blockchain Works
1. **Genesis Block**: Created automatically when the `Blockchain` class is instantiated.
2. **Mining a Block**:
   - The proof-of-work algorithm searches for a valid number that meets the difficulty condition.
   - A new block is created with the proof and the previous block's hash.
   - The block is added to the chain.
3. **Chain Validation**:
   - Ensures that the `previous_hash` of each block matches the actual hash of the previous block.
   - Checks that the proof-of-work condition is met for every block.

## Example Usage
```sh
# Start the Flask server
python app.py

# Mine a new block
curl http://127.0.0.1:5000/mine_block

# Get the blockchain
curl http://127.0.0.1:5000/get_chain

# Validate blockchain
curl http://127.0.0.1:5000/valid
```

