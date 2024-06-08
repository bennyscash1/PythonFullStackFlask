import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(r"db_firebase\db_secret.json")
firebase_admin.initialize_app(cred)


db_connect= firestore.client()

data={

}

doc_refrence= db_connect.collection('WebCollection').document()
doc_refrence.set(data)
print('Document id:', doc_refrence.id)