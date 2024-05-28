import io
import sys
from flask import Flask, render_template, render_template_string, request
import subprocess
import os

import pytest

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        # Collect user inputs from the form
        base_url = request.form['BaseUrl']
        xpath_fields = request.form.getlist('xpathField[]')
        input_strings = request.form.getlist('inputString[]')
        xpath_clicks = request.form.getlist('xpathClick[]')
        xpath_assert = request.form.getlist('xpathAssert[]')
        
        test_dir = os.path.join(os.path.dirname(__file__), 'WebTest', 'Test', 'LoginTest')
        os.makedirs(test_dir, exist_ok=True)

        with open(os.path.join(test_dir, 'user_inputs.txt'), 'w') as f:
            f.write(f"{base_url}\n")
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
            pytest.main(["-x", "WebTest\\Test\\LoginTest\\test_web.py", "-vv"])
            # Run pytest with the specified arguments
        finally:
            # Reset stdout and stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        # Get the output from the StringIO objects
        stdout_output = stdout.getvalue()
        stderr_output = stderr.getvalue()

        result = f"<pre>{stdout_output}</pre><br><pre>{stderr_output}</pre>"
        
        # Display the result on the webpage

    return render_template('indexWebTest.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
