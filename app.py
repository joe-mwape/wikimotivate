from flask import Flask, request, jsonify
from subprocess import Popen, PIPE
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello, this is your Flask server!'

@app.route('/run-script', methods=['POST'])
def run_script():
    process = Popen(['python', 'main.py'], stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    result = {
        'output': output.decode(),
        'error': error.decode()
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False, port=5000)