from database import Base
from sqlalchemy import Column, Integer, String,Float,DateTime, func


class MMSParam(Base):
    __tablename__ = 'mms_param'
    
    registered_at = Column(DateTime,server_default=func.now())
    name = Column(String(length=50), primary_key=True)
    address = Column(Integer,unique=True)
    type = Column(Integer)
    remark = Column(String)