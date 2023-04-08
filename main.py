# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import router

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["127.0.0.1:8000", "localhost:8000"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.include_router(router)
