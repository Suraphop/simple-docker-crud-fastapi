from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import desc
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from starlette import status
from utils import csv
from models import MMSParam
from utils.manage_mms_param import DropDuplicateMMSParam
import pandas as pd
from utils.csv import parse_csv

router = APIRouter(
    prefix='/mms_param',
    tags=['mms_param']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
class MMSParamRequest(BaseModel):
    name : str
    address : str
    type : int
    remark : str

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
async def read_all(db: db_dependency):
    
    mms_param_model = db.query(MMSParam).all()
    if mms_param_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='MMS param not found.')
    return mms_param_model


@router.get("/get_param")
async def get_param(db: db_dependency):
    
    get_param_model = db.query(MMSParam.name,MMSParam.address,MMSParam.type).all()
    df_param_model = pd.DataFrame(get_param_model)
  
    if get_param_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='get param not found.')
    return parse_csv(df_param_model)

@router.post("/upload",status_code=status.HTTP_201_CREATED)
async def create_mms_param(db:db_dependency,file: UploadFile = File(...)):
    
    df = DropDuplicateMMSParam(csv.read_csv(file),db)

    if df.empty:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='dataframe dont have new datas.')
    df.to_sql(name='mms_param',con=engine,if_exists='append',index=False)
    

@router.put("/update/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def update_capacity( db: db_dependency,
                      mms_param_request: MMSParamRequest,
                      name: str):

    mms_param_model = db.query(MMSParam).filter(MMSParam.name == name).first()
    if mms_param_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='name not found.')

    mms_param_model.registered_at = datetime.now()
    mms_param_model.name = mms_param_request.name
    mms_param_model.address = mms_param_request.address
    mms_param_model.type = mms_param_request.type
    mms_param_model.remark = mms_param_request.remark
    db.add(mms_param_model)
    db.commit()

@router.delete("/delete/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_capacity(db: db_dependency, name: str):
    mms_param_model = db.query(MMSParam).filter(MMSParam.name == name).first()
    if mms_param_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='name not found.')
    db.query(MMSParam).filter(MMSParam.name == name).delete()
    db.commit()