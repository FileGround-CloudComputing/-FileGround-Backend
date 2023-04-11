# main.py

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from router import router

app = FastAPI()


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        # you probably want some kind of logging here
        return Response("Internal server error", status_code=500)
app.middleware('http')(catch_exceptions_middleware)

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.include_router(router)
