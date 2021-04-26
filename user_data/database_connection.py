from google.cloud import firestore

#Initialize an instance of Firestore
db = firestore.Client()

doc_collection = db.collection(u'counting')