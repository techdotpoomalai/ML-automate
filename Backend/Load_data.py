from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import numpy as np
import pandas as pd
import chardet
import json
import io

import pandas as pd

class Load_data:
    def __init__(self,):
        pass

    def get_data(self,):
        try:
            # Detect encoding of the CSV file
            with open('data.csv', 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']
            # Read CSV with the detected encoding
            df = pd.read_csv('data.csv', encoding=encoding)

            response_dict = df.to_dict(orient='records')
            for record in response_dict:
                for key, value in record.items():
                    if pd.isna(value):  # Check if the value is NaN using pandas' pd.isna() function
                        record[key] = ''  # Replace NaN with an empty string

            return response_dict
        except Exception as e:
            print(f"Error: {e}")
            result = []

        return result
        
    def get_describ(self,):
        try:
            df = pd.read_csv("preprocess.csv")
            des={}
            num_rows, num_columns = df.shape
            describ = list(dict(df.dtypes).items())
            
            for col in describ:
               des[col[0]] = str(col[1])
            return [num_rows, num_columns, des]         
        except:
            return []
        
    async def save_file(self, file: UploadFile):
        res={}
        try:
            with open("data.csv", 'wb') as f:
                f.write(await file.read()) 
            res['message']='success'
            describ= self.get_describ()
            res['rows'] = describ[0]
            res['columns'] = describ[1]
            res['describtion'] = describ[2]
            return JSONResponse(res)
        except Exception as e:
            return f"error: {str(e)}"

    
