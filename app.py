from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect user inputs from the form
        base_url = request.form['BaseUrl']
        xpath_fields = request.form.getlist('xpathField[]')
        input_strings = request.form.getlist('inputString[]')
        xpath_clicks = request.form.getlist('xpathClick[]')
        test_dir = os.path.join(os.path.dirname(__file__), 'WebTest', 'Test', 'LoginTest')
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir, 'user_inputs.txt'), 'w') as f:
            f.write(f"{base_url}\n")
            for xpath, string in zip(xpath_fields, input_strings):
                f.write(f"{xpath}\n{string}\n")
            for xpath_click in xpath_clicks:
                f.write(f"{xpath_click}\n")

        # Run pytest with the test file
        result = subprocess.Popen(["pytest", "WebTest\\Test\\LoginTest\\test_login.py"], capture_output=True, text=True)

        # Display the result on the webpage
        return f"<pre>{result.stdout}</pre><br><pre>{result.stderr}</pre>"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
