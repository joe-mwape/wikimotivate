from flask import Flask, render_template, request, jsonify
from subprocess import Popen, PIPE
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    process = Popen(['python', 'main.py'], stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    result = {
        'output': output.decode(),
        'error': error.decode()
    }
    return jsonify(result)

#if __name__ == '__main__':
  #app.run(debug=True, host='0.0.0.0', port=5000)