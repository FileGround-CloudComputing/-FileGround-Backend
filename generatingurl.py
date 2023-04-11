from fastapi import FastAPI
import datetime
import os
from google.cloud import storage

app = FastAPI()

@app.get("/")
async def hello():
    return {"msg":"this is API server"}

@app.post("/ground/:gid/photo")
async def generate_upload_signed_url(file_name):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="config/serviceAccountKey.json" # 서비스 키 값
    
    storage_client = storage.Client()
    bucket = storage_client.bucket('new-tori-bucket') #bucket name
    blob = bucket.blob(file_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 30 minutes
        expiration=datetime.timedelta(minutes=30),
        # Allow PUT requests using this URL.
        method="PUT",
    )
    return url

@app.get("/ground/:gid/photo")
async def generate_download_signed_url(file_name):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="config/serviceAccountKey.json" # 서비스 키 값
    storage_client = storage.Client()
    bucket = storage_client.bucket('new-tori-bucket') #bucket name
    blob = bucket.blob(file_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )
    return url

