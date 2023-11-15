from flask import Flask, render_template, request, jsonify
from subprocess import Popen, PIPE
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Set the path to the 'templates' directory (assuming 'app.py' is in the parent directory)
templates_path = os.path.join(os.path.dirname(__file__), 'templates')

@app.route('/')
def index():
    # Construct the full path to the index.html file within the 'templates' folder
    index_path = os.path.join(templates_path, 'index.html')
    return render_template(index_path)

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
