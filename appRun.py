import io
import sys
from flask import Flask, render_template, request, jsonify
import subprocess
import os
import pytest
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS


# Initialize .env file
load_dotenv() 

# Initialize Flask app
app = Flask(__name__)
# TODO REMOVE THIS BEFORE DEPLOYMENT
CORS(app, origins=["http://localhost:3000"])

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"db_firebase/db_secret.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/runTest', methods=['POST'])
def run_test():
    data = request.json
    test_name = data.get('testName')

    if not test_name:
        return jsonify({"error": "Test name is required"}), 400

    # Fetch test data from Firestore
    tests_ref = db.collection('WebCollection')
    query = tests_ref.where('testName', '==', test_name).stream()

    test_data = None
    for doc in query:
        test_data = doc.to_dict()
        break

    if not test_data:
        return jsonify({"error": "Test not found"}), 404

    # Run the test
    stdout = io.StringIO()
    stderr = io.StringIO()
    sys.stdout = stdout
    sys.stderr = stderr

    try:
        pytest.main(["-x", "WebTest/Test/test_web.py", "-vv"])
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    stdout_output = stdout.getvalue()
    stderr_output = stderr.getvalue()

    return jsonify({"stdout": stdout_output, "stderr": stderr_output}), 200

if __name__ == '__main__':
    app.run(debug=True)
