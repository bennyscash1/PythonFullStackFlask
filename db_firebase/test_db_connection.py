import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(r"db_firebase\pythonfullstackflask-firebase-adminsdk-qmrb6-4b41a4d418.json")
firebase_admin.initialize_app(cred)


db_connect= firestore.client()

data={
    'Base url': 'input url data',
    'input field': {
        'xpath locator': 'input locator xpath data',
        'input string': 'input string data'
    },
    'Button locator': 'button locator xpath data',
    'Assert locator': 'assert locator xpath data'
}

doc_refrence= db_connect.collection('WebCollection').document()
doc_refrence.set(data)
print('Document id:', doc_refrence.id)