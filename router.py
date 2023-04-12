# views.py
import random
import json
from datetime import timedelta, datetime
import firebase_admin
from firebase_admin import credentials, firestore, db
from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel


from services import login_service
from services import test_login_service


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

router = APIRouter()

cred = credentials.Certificate(
    "serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://file-ground-default-rtdb.asia-southeast1.firebasedatabase.app'}
                              )

# Get Firestore client
dbs = firestore.client()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@router.get("/naver/login")
async def naver_login(request: Request, Authorize: AuthJWT = Depends()):
    redirect_uri = request.url_for("naver_callback")
    print('redirect_uri:', redirect_uri)
    naver_login_url = login_service.get_naver_login_url(redirect_uri)
    return HTMLResponse(f'<h1><a href="{naver_login_url}">Sign in with Naver</a></h1>')


@router.get("/naver/callback")
async def naver_callback(request: Request, response: Response, code: str = None, state: str = None, Authorize: AuthJWT = Depends()):
    if code is None or state is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Missing code or state parameter")
    login_token = await login_service.get_naver_login_token(code, state)
    response.set_cookie(key="access_token", value=login_token["access_token"])
    return login_token
    # return {"access_token": login_token["access_token"]}


@router.get("/")
async def root(Authorize: AuthJWT = Depends()):
    return {"message": "Hello World oh yeah sumin is legend"}


@router.post("/users")
async def create_user(user: dict, Authorize: AuthJWT = Depends()):
    # Add new user to Realtime Database Firebase
    ref = db.reference("/users/" + user["id"])
    ref.push().set(user)
    # Add new user document to Firestore
    doc_ref = dbs.collection(u'users').document(user["id"])
    doc_ref.set(user)

    return {"message": "User created successfully"}


@router.get("/users")
async def get_users(user_id: str, Authorize: AuthJWT = Depends()):
    # Retrieve user from RealtimeDatabase
    ref = db.reference("/users")
    user_info = ref.get()
    return_dict = {}
    for key, value in user_info.items():
        return_dict[key] = value
    # Retrieve user document from Firestore
    doc_ref = dbs.collection(u'users').document(user_id)
    doc = doc_ref.get()


@router.get("/users/{user_id}")
async def get_user(user_id: str, Authorize: AuthJWT = Depends()):
    # Retrieve user from RealtimeDatabase
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


@router.post("/photos")
async def upload_photo(photo: dict, Authorize: AuthJWT = Depends()):
    # firebase storage connect
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="serviceAccountKey.json" # service account key path
    storage_client = storage.Client()
    bucket = storage_client.bucket('your-bucket-name') #bucket name
    blob = bucket.blob(photo["title"])

    url = blob.generate_signed_url(
        version="v4",        
        expiration=datetime.timedelta(minutes=30), # This URL is valid for 30 minutes
        method="PUT", # Allow PUT requests using this URL.
    )

    # Add new photo to Realtime Database Firebase
    ref = db.reference("/photos/" + photo["id"])
    ref.push().set(photo)
    # Add new photo document to Firestore
    doc_ref = dbs.collection(u'photos').document(photo["id"])
    doc_ref.set(photo)

    return url


@router.get("/photos/{photo_id}")
async def get_photo(photo_id: str, Authorize: AuthJWT = Depends()):
    # Retrieve user from RealtimeDatabase
    ref = db.reference("/photos/" + photo_id)
    photo_info = ref.get()
    return_dict = {}
    for key, value in photo_info.items():
        return_dict[key] = value
    # Retrieve user document from Firestore
    doc_ref = dbs.collection(u'photos').document(photo_id)
    doc = doc_ref.get()
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="service-key-path.json" # 서비스 키 값
    storage_client = storage.Client()
    bucket = storage_client.bucket('your-bucket-name') #bucket name
    blob = bucket.blob(doc_ref.get('photo_name'))

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )

    return url


@router.post("/ground")
async def create_ground(ground: dict, Authorize: AuthJWT = Depends()):
    # Add new user to Realtime Database Firebase
    while (True):
        random_num = random.randint(100000, 999999)
        id = random_num
        ref = db.reference("/ground/")
        ground_info = ref.get()

        if ground_info == "'None'":
            ground["id"] = str(id)
            break

        bool = False
        for key, value in ground_info.items():
            if value["id"] == id:
                bool = True
        if bool == False:
            print(id)
            ground["id"] = str(id)
            break

    ref = db.reference("/ground/" + str(ground["id"]))
    ref.set(ground)

    return {"message": "User created successfully"}


@router.get("/ground/{ground_id}")
async def get_ground(ground_id: str, Authorize: AuthJWT = Depends()):
    # Retrieve user from RealtimeDatabase
    ref = db.reference("/ground/" + ground_id)
    ground_info = ref.get()
    return_dict = {}
    for key, value in ground_info.items():
        return_dict[key] = value
    return return_dict


@router.post("/auth/access")
async def renew_access_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    print('current_user:', db.reference('/uers').get(current_user))
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {
        "accessToken": new_access_token,
        "accessTokenExpiresIn": datetime.today().isoformat()
    }


@router.post("/auth/refresh")
async def renew_refresh_token(Authorize: AuthJWT = Depends()):
    current_user = Authorize.get_jwt_subject()
    if current_user is None:
        print("기본 유저인 박선우로 세팅합니다")
        return {
            "accessToken": Authorize.create_access_token(subject="63d52530-d872-11ed-8a0c-00155d2526d3"),
            "refreshToken": Authorize.create_refresh_token(subject="63d52530-d872-11ed-8a0c-00155d2526d3"),
            "accessTokenExpiresIn": datetime.today().isoformat(),
            "refreshTokenExpiresIn": datetime.today().isoformat()
        }
    access_token = Authorize.create_access_token(subject=current_user)
    refresh_token = Authorize.create_refresh_token(subject=current_user)
    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "accessTokenExpiresIn": datetime.today().isoformat(),
        "refreshTokenExpiresIn": datetime.today().isoformat()

    }
