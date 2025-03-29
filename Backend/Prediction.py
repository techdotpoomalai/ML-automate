import json
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import pickle
import pandas as pd

from Preprocess import Preprocess

label_encoder = LabelEncoder()
onehot_encoder=OneHotEncoder()

class Prediction(Preprocess):
    def __init__(self):
        super().__init__()
        self.fited_onehot_encode=None

    def get_data(self):
        return super().get_data()
    
    def process(self, col, prepros):
        return super().process(col, prepros)
    
    def get_json_input(self,):
        json_input={
            "number":[],
            "text":[]
        }
        try:
            df = pd.read_csv(f"data.csv")
            cols=df.columns.to_list()
            temp1={}
            for col in cols:
                if df[col].dtype == object:
                    temp2=df[col].unique().tolist()
                    temp1[col]=temp2
                else:
                    json_input["number"].append(col)
            json_input["text"]=temp1
            return json_input
        except:
            return {"message":"fail"}

    def find(self, pridict_input):
        return super().find(pridict_input)    
       