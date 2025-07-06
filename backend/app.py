from flask import Flask, request, jsonify
from flask_cors import CORS
from junklang.interpreter import run_junk_code

app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST', 'OPTIONS'])
def run_code():
    if request.method == 'OPTIONS':
        return '', 204

    code = request.json.get('code', '')
    output = run_junk_code(code)
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
