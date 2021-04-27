import os
from google.cloud import firestore
from firebase_admin import credentials, initialize_app

#Initialize an instance of Firestore
data = os.path.abspath(os.path.dirname(__file__)) + "/key.json"
cred = credentials.Certificate(data)
default_app = initialize_app(cred)

db = firestore.Client()
doc_collection = db.collection(u'counting')