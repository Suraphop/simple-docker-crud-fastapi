from io import BytesIO
import json
import pandas as pd

def read_csv(file):
    ''' read csv file then return to df'''
    contents = file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer)
    buffer.close()
    file.file.close() 
    return df

def parse_csv(df):
    '''convert df to json'''
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed