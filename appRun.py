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

def handle_request(template_name):
    result = ""
    if request.method == 'POST':
        if template_name == 'indexMobileTest.html':
            # Collect mobile-specific user inputs from the form
            app_package = request.form['appPackage']
            app_activity = request.form['appActivity']
            udid = request.form['udid']
        else:
            # Collect web-specific user inputs from the form
            base_url = request.form['BaseUrl']

        xpath_fields = request.form.getlist('xpathField[]')
        input_strings = request.form.getlist('inputString[]')
        xpath_clicks = request.form.getlist('xpathClick[]')
        xpath_assert = request.form.getlist('xpathAssert[]')

        if template_name == 'indexMobileTest.html':
            test_dir = os.path.join(os.path.dirname(__file__), 'MobileTest', 'MobileTest')
        else:
            test_dir = os.path.join(os.path.dirname(__file__), 'WebTest', 'Test', 'LoginTest')
        
        os.makedirs(test_dir, exist_ok=True)

        with open(os.path.join(test_dir, 'user_inputs.txt'), 'w') as f:
            if template_name == 'indexMobileTest.html':
                f.write(f"AppPackage: {app_package}\n")
                f.write(f"AppActivity: {app_activity}\n")
                f.write(f"UDID: {udid}\n")
            else:
                f.write(f"BaseUrl: {base_url}\n")

            for xpath, string in zip(xpath_fields, input_strings):
                f.write(f"InputXpath: {xpath}, {string}\n")
            for xpath_click in xpath_clicks:
                f.write(f"ButtonAction: {xpath_click}\n")
            for xpath_assert in xpath_assert:
                f.write(f"AssertXpath: {xpath_assert}\n")

        # Run pytest with the test file
        stdout = io.StringIO()
        stderr = io.StringIO()
        sys.stdout = stdout
        sys.stderr = stderr

        try:
            if template_name == 'indexMobileTest.html':
                pytest.main(["-x", "MobileTest\\MobileTest\\test_mobile.py", "-vv"])
            else:
                pytest.main(["-x", "WebTest\\Test\\LoginTest\\test_web.py", "-vv"])
        finally:
            # Reset stdout and stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        # Get the output from the StringIO objects
        stdout_output = stdout.getvalue()
        stderr_output = stderr.getvalue()

        result = f"<pre>{stdout_output}</pre><br><pre>{stderr_output}</pre>"

    return render_template(template_name, result=result)

if __name__ == '__main__':
    app.run(debug=True)
