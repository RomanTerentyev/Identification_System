from flask import  Flask, jsonify, request
import Calculations

app = Flask(__name__)

@app.route('/identification', methods=["POST"])
def faces():
    result = Calculations.recognition(request.get_json(force = True))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug = True, port=5000)
