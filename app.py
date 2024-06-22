from flask import Flask, request, render_template, jsonify
from web3 import Web3
import json

app = Flask(__name__)

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
contract_address = '0xYourContractAddress'  # Update with your contract address
with open('build/contracts/LandRegistry.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contract_info', methods=['GET'])
def contract_info():
    return jsonify({
        'address': contract_address,
        'abi': contract_abi
    })

@app.route('/get_history', methods=['GET'])
def get_history():
    uid = int(request.args.get('uid'))
    record = contract.functions.records(uid).call()

    record_data = {
        'name': record[0],
        'age': record[1],
        'landHistory': record[2],
        'timestamp': record[3],
        'owner': record[4]
    }

    return render_template('record.html', record=record_data)

@app.route('/view_blockchain', methods=['GET'])
def view_blockchain():
    record_count = contract.functions.recordCount().call()
    records = []
    for uid in range(record_count):
        record = contract.functions.records(uid).call()
        records.append({
            'uid': uid,
            'name': record[0],
            'age': record[1],
            'landHistory': record[2],
            'timestamp': record[3],
            'owner': record[4]
        })
    
    return render_template('blockchain.html', records=records)

if __name__ == '__main__':
    app.run()
