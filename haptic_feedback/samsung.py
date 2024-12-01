from flask import Flask

app = Flask(__name__)

@app.route('/vibrate', methods=['GET'])
def vibrate():
    return "Vibration command received!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
