from fastapi import  FastAPI
from router import mms_param
from database import engine
from fastapi.middleware.cors import CORSMiddleware

import models


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

app.include_router(mms_param.router)