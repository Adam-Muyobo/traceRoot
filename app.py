from flask import Flask, render_template, request, redirect, url_for
import datetime
import hashlib
import json
import qrcode
import os

app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        value = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode()
        return hashlib.sha256(value).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data="Genesis Block",previous_hash='0')

    def create_block(self, data=None, previous_hash=None):
        block = Block(len(self.chain), datetime.datetime.now().isoformat(), data, previous_hash)
        self.chain.append(block.__dict__)
        return block

    def last_block(self):
        return self.chain[-1]

blockchain = Blockchain()

# Generate QR Code for block data
def generate_qr_code(data, filename):
    qr = qrcode.make(data)
    qr.save(os.path.join('static', filename))
    return filename

@app.route('/')
def home():
    qr_codes = []
    for block in blockchain.chain:
        qr_code_filename = f"block_{block['index']}.png"
        qr_codes.append(generate_qr_code(str(block), qr_code_filename))

    return render_template('index.html', chain=blockchain.chain, qr_codes=qr_codes, zip=zip)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.form['data']
    last_block = blockchain.last_block()
    blockchain.create_block(data, last_block['hash'])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
