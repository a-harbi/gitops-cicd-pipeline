from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def root():
    return "Backend is alive!\n"

@app.route("/api/data")
def data():
    # In a real app you'd talk to the database here.
    msg = os.getenv("BACKEND_MESSAGE", "Hello from the backend!")
    return jsonify({"message": msg})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
