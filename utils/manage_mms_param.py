import pandas as pd

from models import MMSParam


def DropDuplicateMMSParam(df,db):
    '''check dupicate between sql server and new df then return df that not duplicate yet'''
    mms_param_model = pd.DataFrame(db.query(MMSParam.name).all(),columns=['name'])
    drop_dubplicate = df.merge(mms_param_model, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
    return drop_dubplicate