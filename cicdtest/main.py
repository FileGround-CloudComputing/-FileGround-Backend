import firebase_admin
from firebase_admin import credentials, firestore, db
from fastapi import FastAPI
import json

app = FastAPI()

# Initialize Firebase credentials
cred = credentials.Certificate("sunwutest-5c812-firebase-adminsdk-3983l-1239db8abf.json")
firebase_admin.initialize_app(cred,
                              {'databaseURL':'https://sunwutest-5c812-default-rtdb.asia-southeast1.firebasedatabase.app/'})

# Get Firestore client
dbs = firestore.client()

@app.get("/")
async def root():
    return {"message": "Hello World oh yeah"}


@app.post("/users")
async def create_user(user: dict):
    #Add new user to Realtime Database Firebase
    ref = db.reference("/users/" + user["id"])
    ref.push().set(user)
    # Add new user document to Firestore
    doc_ref = dbs.collection(u'users').document(user["id"])
    doc_ref.set(user)

    return {"message": "User created successfully"}

@app.get("/users")
async def get_users(user_id: str):
    #Retrieve user from RealtimeDatabase
    ref = db.reference("/users")
    user_info = ref.get()
    return_dict = {}
    for key, value in user_info.items():
        return_dict[key] = value
    # Retrieve user document from Firestore
    doc_ref = dbs.collection(u'users').document(user_id)
    doc = doc_ref.get()


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    #Retrieve user from RealtimeDatabase
    ref = db.reference("/users/" + user_id)
    user_info = ref.get()
    return_dict = {}
    for key, value in user_info.items():
        return_dict[key] = value
    # Retrieve user document from Firestore
    doc_ref = dbs.collection(u'users').document(user_id)
    doc = doc_ref.get()

    return return_dict.items()

    if doc.exists:
        return doc.to_dict()
    else:
        return {"message": "User not found"}
    
@app.post("/photos")
async def upload_photo(photo: dict):
    #Add new photo to Realtime Database Firebase
    ref = db.reference("/photos/" + photo["id"])
    ref.push().set(photo)
    # Add new photo document to Firestore
    doc_ref = dbs.collection(u'photos').document(photo["id"])
    doc_ref.set(photo)

    return {"message": "Photo created successfully"}

@app.get("/photos/{photo_id}")
async def get_photo(photo_id: str):
    #Retrieve user from RealtimeDatabase
    ref = db.reference("/photos/" + photo_id)
    photo_info = ref.get()
    return_dict = {}
    for key, value in photo_info.items():
        return_dict[key] = value
    # Retrieve user document from Firestore
    doc_ref = dbs.collection(u'photos').document(photo_id)
    doc = doc_ref.get()

    return return_dict.items()

    if doc.exists:
        return doc.to_dict()
    else:
        return {"message": "User not found"}
    
@app.post("/ground")
async def create_ground(ground: dict):
    #Add new user to Realtime Database Firebase
    ref = db.reference("/ground/" + ground["id"])
    ref.push().set(ground)
    # Add new user document to Firestore
    doc_ref = dbs.collection(u'ground').document(ground["id"])
    doc_ref.set(ground)

    return {"message": "User created successfully"}

@app.get("/ground/{ground_id}")
async def get_ground(ground_id: str):
    #Retrieve user from RealtimeDatabase
    ref = db.reference("/ground/" + ground_id)
    ground_info = ref.get()
    return_dict = {}
    for key, value in ground_info.items():
        return_dict[key] = value
    # Retrieve user document from Firestore
    doc_ref = dbs.collection(u'ground').document(ground_id)
    doc = doc_ref.get()

    return return_dict.items()

    if doc.exists:
        return doc.to_dict()
    else:
        return {"message": "User not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
