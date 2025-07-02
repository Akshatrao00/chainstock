from web3 import Web3

# ✅ Step 1: Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
assert web3.is_connected(), "❌ Unable to connect to Ganache"
print("✅ Connected to Ganache")

# ✅ Step 2: Set your deployed contract address from Remix
contract_address = web3.to_checksum_address("0xA7e7eF5EEC2cE78Bb7Ae3C784D49D29d2Ee0cC02")  # Replace this

# ✅ Step 3: Contract ABI (from Remix after compile)
contract_abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "lat", "type": "string"},
            {"internalType": "string", "name": "longi", "type": "string"}
        ],
        "name": "addLocation",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"}
        ],
        "name": "getLocation",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "string", "name": "", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# ✅ Step 4: Your Ganache account details
sender = web3.to_checksum_address("0x8dbcAA407f951FD2149cF8b1Aed72Dc78af21010")
private_key = "0x0db4bdb6488cfc66918dcf90999e3cea4f3bf58f68629907318f0f098bb99c40"

# ✅ Step 5: Load the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# ✅ Step 6: Prepare data
latitude = "26.8500"
longitude = "80.949997"

# ✅ Step 7: Build transaction
nonce = web3.eth.get_transaction_count(sender)
txn = contract.functions.addLocation(latitude, longitude).build_transaction({
    'chainId': 1337,
    'gas': 2000000,
    'gasPrice': web3.to_wei('50', 'gwei'),
    'nonce': nonce
})

# ✅ Step 8: Sign and send transaction
signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
print("🚀 Transaction sent! Hash:", txn_hash.hex())

# ✅ Step 9: Wait for confirmation
receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
print("✅ Transaction mined.")

# ✅ Step 10: Retrieve stored location
(lat, longi) = contract.functions.getLocation(sender).call()
print(f"📍 Stored Location: Latitude = {lat}, Longitude = {longi}")
