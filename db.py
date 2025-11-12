import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def clear_collection(collection_name):
    docs = db.collection(collection_name).stream()
    for doc in docs:
        doc.reference.delete()

def db_add(entry, collection_name):
	db.collection(collection_name).document(str(entry["id"])).set(entry)
