from flask import Flask, request, jsonify


app = Flask(__name__)

# A simple in-memory database for demonstration purposes (replace with a real database)
user_db = {
    "username": "admin",
    "password": "j5"
}

@app.route('/', methods=['GET'])
def hello():
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
    

    username = request.json.get('username')
    password = request.json.get('password')

    # Check if 'username' and 'password' keys are in the JSON data
    if not 'username' or not 'password':
        return jsonify({"message": "Missing 'username' or 'password' in JSON data"}), 400

    # Check if the username exists and the password matches
    if user_db['username'] == username and user_db['password'] == password:
        return jsonify({"message": "Login successful"}), 200
    elif user_db['username'] == username and user_db['password'] != password:
        return jsonify({"message": "Login failed"}), 401
    else:
        return jsonify({"message": "Something went wrong"}), 500



@app.route('/agents', methods=['GET'])
def agents():
    user_agent = request.headers.get('User-Agent')
    if(user_agent == "MyCustomUserAgent/1.0"):
        return jsonify({"message":f"request from agent: {user_agent}"}), 400
    else:
        return jsonify({"message":f"request from agent: {user_agent}"}), 200



if __name__ == '__main__':
    port = 9541

    app.run(debug=True, port=port)
