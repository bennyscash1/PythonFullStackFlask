import requests
import os

class PageOutputDTO:
    def __init__(self, page):
        self.result = {"page": page}
    def to_json(self):
        return self.data

def test_api():
    # Read user inputs from the file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(test_dir, 'user_inputs.txt'), 'r') as f:
        lines = f.readlines()
        inputs = {}
        post_keys = []
        post_values = []
        for line in lines:
            key, value = line.split(': ')
            key = key.strip()
            value = value.strip()
            if key == "PostKey":
                post_keys.append(value)
            elif key == "PostValue":
                post_values.append(value)
            else:
                inputs[key] = value
        
        data = {key: post_values[i] for i, key in enumerate(post_keys)}

    url = inputs.get("APIEndpoint")
    headers = {"Authorization": inputs.get("Headers", "")}
    expected_response = int(inputs.get("AssertStatus"))
    
    if inputs.get("RequestType") == "POST":
        response = requests.post(url, headers=headers, json=data)
        assert response.status_code == expected_response, f"----Expected status: {expected_response}, Actual status: {response.status_code},  Response JSON: {response.json()}-----"

  
    else:
        response = requests.get(url, headers=headers)
        assert response.status_code == expected_response, f"-----Expected status: {expected_response}, Actual status: {response.status_code}----"
        
        
