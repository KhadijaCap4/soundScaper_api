import firebase_admin
from firebase_admin import credentials
import pyrebase
from configs.firebase_config_example import firebaseConfig

if not firebase_admin._apps:
    cred = credentials.Certificate("configs/soundscaper-98b5b-firebase-adminsdk-bwf3k-13f6b4e070.json")
    firebase_admin.initialize_app(cred)
    
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
authUser = firebase.auth()