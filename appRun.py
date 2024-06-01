import io
import sys
from flask import Flask, render_template, request
import subprocess
import os
import pytest

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mobileTest', methods=['GET', 'POST'])
def mobile_index():
    return handle_request('indexMobileTest.html')

@app.route('/webTest', methods=['GET', 'POST'])
def web_index():
    return handle_request('indexWebTest.html')

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
            
        elif template_name == 'indexApiTest.html':
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

if __name__ == '__main__':
    app.run(debug=True)
