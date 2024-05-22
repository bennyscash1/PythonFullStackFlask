import requests
import GetData
from GetData import VarData, data
class RegisterInputDTO:
    def __init__(self, email, password):
        self.data = {"email": email, "password": password}
    def to_json(self):
        return self.data
class RegisterOutputDTO:
    def __init__(self, id, token):
        self.result = {"id": id, "token": token}
    def to_json(self):
        return self.data

def test_baba():
    #Test data
    url = GetData.loaded_data[VarData.BaseApiUrl] +"register"
    email = GetData.loaded_data[VarData.ApiEmail]
    password = GetData.loaded_data[VarData.ApiPassword]

    #requst data
    registration_data = RegisterInputDTO(email, password)
    bearer_token = "your_bearer_token_here"
    headers_with_token = GetData.get_headers(include_token=True, bearer_token=bearer_token)

    response = requests.post(url,
                             json=registration_data.to_json(),
                             headers=headers_with_token)

    assert response.status_code == 200
    response_data = response.json()
    output_dto = RegisterOutputDTO(response_data['id'], response_data['token'])
    print("id:", output_dto.result['id'])
    print("token:", output_dto.result['token'])
    assert  output_dto.result['id']==4
