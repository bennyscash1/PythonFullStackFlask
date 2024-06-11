import io
import sys
from flask import Flask, render_template, request, jsonify
import subprocess
import os
import pytest
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Inititalize .env file
load_dotenv() 

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"db_firebase/db_secret.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    tests_ref = db.collection('WebCollection')
    tests = [doc.to_dict() for doc in tests_ref.stream()]
    return render_template('home.html', tests=tests)

@app.route('/mobileTest', methods=['GET', 'POST'])
def mobile_index():
    return handle_request('indexMobileTest.html')

@app.route('/webTest', methods=['GET', 'POST'])
def web_index():
    return handle_request('/webTemplates/indexWebTest.html')

@app.route('/webTemplates/editTest.html')
def edit_test():
    test_name = request.args.get('testName')
    if not test_name:
        return "Test name is required", 400

    print(f"Fetching test data for: {test_name}")

    # Query Firestore for the document with the specified testName
    tests_ref = db.collection('WebCollection')
    query = tests_ref.where('testName', '==', test_name).stream()
    
    test_data = None
    for doc in query:
        test_data = doc.to_dict()
        break

    if not test_data:
        print(f"Test not found: {test_name}")
        return "Test not found", 404

    print(f"Test data fetched: {test_data}")
    return render_template('webTemplates/editTest.html', test=test_data)
#####
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

    # Save test data to a file
    test_dir = os.path.join(os.path.dirname(__file__), 'WebTest', 'Test')
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, 'user_inputs.txt'), 'w') as f:
        f.write(f"BaseUrl: {test_data.get('BaseUrl')}\n")
        for xpath, string in zip(test_data.get('xpathFields', []), test_data.get('inputStrings', [])):
            f.write(f"InputXpath: {xpath}, {string}\n")
        for xpath_click in test_data.get('xpathClicks', []):
            f.write(f"ButtonAction: {xpath_click}\n")
        for xpath_assert in test_data.get('xpathAsserts', []):
            f.write(f"AssertXpath: {xpath_assert}\n")

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

#####

@app.route('/getTestData', methods=['GET'])
def get_test_data():
    test_name = request.args.get('testName')
    if not test_name:
        return jsonify({"error": "Test name is required"}), 400

    tests_ref = db.collection('WebCollection')
    query = tests_ref.where('testName', '==', test_name).stream()
    
    test_data = None
    for doc in query:
        test_data = doc.to_dict()
        break

    if not test_data:
        return jsonify({"error": "Test not found"}), 404

    return jsonify(test_data), 200

@app.route('/apiTest', methods=['GET', 'POST'])
def api_index():
    return handle_request('indexApiTest.html')

def handle_request(template_name):
    result = ""
    if request.method == 'POST':
        if template_name == 'indexMobileTest.html':
            app_package = request.form['appPackage']
            app_activity = request.form['appActivity']
            udid = request.form['udid']
            
        elif template_name == 'webTemplates/indexApiTest.html':
            api_endpoint = request.form['apiEndpoint']
            request_type = request.form['requestType']
            headers = request.form.get('headers', "")
            assert_status = request.form['assertStatus']
            post_keys = request.form.getlist('postKey[]')
            post_values = request.form.getlist('postValue[]')
        else:
            base_url = request.form['BaseUrl']

        xpath_fields = request.form.getlist('xpathField[]')
        input_strings = request.form.getlist('inputString[]')
        xpath_clicks = request.form.getlist('xpathClick[]')
        xpath_assert = request.form.getlist('xpathAssert[]')

        if template_name == 'indexMobileTest.html':
            test_dir = os.path.join(os.path.dirname(__file__), 'MobileTest', 'MobileTest')
        elif template_name == 'indexApiTest.html':
            test_dir = os.path.join(os.path.dirname(__file__), 'ApiTest',)
        else:
            test_dir = os.path.join(os.path.dirname(__file__), 'WebTest', 'Test')
        
        os.makedirs(test_dir, exist_ok=True)

        with open(os.path.join(test_dir, 'user_inputs.txt'), 'w') as f:
            if template_name == 'indexMobileTest.html':
                f.write(f"AppPackage: {app_package}\n")
                f.write(f"AppActivity: {app_activity}\n")
                f.write(f"UDID: {udid}\n")
            elif template_name == 'indexApiTest.html':
                f.write(f"APIEndpoint: {api_endpoint}\n")
                f.write(f"RequestType: {request_type}\n")
                f.write(f"Headers: {headers}\n")
                f.write(f"AssertStatus: {assert_status}\n")
                for key in post_keys:
                    f.write(f"PostKey: {key}\n")
                for value in post_values:
                    f.write(f"PostValue: {value}\n")
            else:
                f.write(f"BaseUrl: {base_url}\n")

            for xpath, string in zip(xpath_fields, input_strings):
                f.write(f"InputXpath: {xpath}, {string}\n")
            for xpath_click in xpath_clicks:
                f.write(f"ButtonAction: {xpath_click}\n")
            for xpath_assert in xpath_assert:
                f.write(f"AssertXpath: {xpath_assert}\n")

        stdout = io.StringIO()
        stderr = io.StringIO()
        sys.stdout = stdout
        sys.stderr = stderr

        try:
            if template_name == 'indexMobileTest.html':
                pytest.main(["-x", "MobileTest/MobileTest/test_mobile.py", "-vv"])
            elif template_name == 'indexApiTest.html':
                pytest.main(["-x", "ApiTest/test_get.py", "-vv"])
            else:
                pytest.main(["-x", "WebTest/Test/test_web.py", "-vv"])
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        stdout_output = stdout.getvalue()
        stderr_output = stderr.getvalue()

        result = f"<pre>{stdout_output}</pre><br><pre>{stderr_output}</pre>"

    return render_template(template_name, result=result)

@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    try:
        # Assuming you have a unique field 'testName' in your document
        test_name = data['testName']
        # Query the document ID based on the test name
        tests_ref = db.collection('WebCollection')
        query = tests_ref.where('testName', '==', test_name).stream()
        
        doc_id = None
        for doc in query:
            doc_id = doc.id
            break

        if doc_id:
            db.collection('WebCollection').document(doc_id).set(data)
        else:
            db.collection('WebCollection').add(data)

        return jsonify({"message": "Data saved successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Error saving data", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
