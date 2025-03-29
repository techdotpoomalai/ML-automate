import json
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, LabelEncoder,OneHotEncoder
from sklearn.pipeline import Pipeline
import pickle

from Load_data import Load_data

onehot_encoder = OneHotEncoder()

class Preprocess(Load_data):
    def __init__(self):
        super().__init__()
        self.prepros_record={}
        self.label_encoders={}
        self.onehot_encoded_status=False
        self.label_encoder_status=False

    def get_data(self):
        self.prepros_record={
            'onehot_encode':[],
            'label_encode':[],
            'drop_col':[]
        }
        return super().get_data()
    
    

    def process(self,col,prepros):
        # print(col,prepros)
        col_dict=json.loads(col)
        cols=[key for key, value in col_dict.items() if value]
        try:
            df = pd.read_csv(f"preprocess.csv")
            if prepros == 'onehot_encode':
                onehot_encoder.fit(df[cols])
                self.onehot_encoded_status=True
                encoded = onehot_encoder.transform(df[cols])
                encoded_columns = onehot_encoder.get_feature_names_out(cols)
                encoded_df = pd.DataFrame(encoded.toarray(), columns=encoded_columns)
                df.drop(columns=cols, inplace=True)
                df = pd.concat([encoded_df, df], axis=1)

                temp=[]
                if self.prepros_record['onehot_encode']:
                    temp=self.prepros_record['onehot_encode']
                temp.extend(cols)
                self.prepros_record['onehot_encode']=temp
                

            elif prepros == 'label_encode':
                for col_name in cols:
                    label_encoder = LabelEncoder()
                    df[col_name] = label_encoder.fit_transform(df[col_name])
                    self.label_encoder_status=True
                    self.label_encoders[col_name] = label_encoder
            
                temp=[]
                if self.prepros_record['label_encode']:
                    temp=self.prepros_record['label_encode']
                temp.extend(cols)
                self.prepros_record['label_encode']=temp
                    
            elif prepros == 'drop_col':
                df.drop(columns=cols, errors='ignore', inplace=True)

                temp=[]
                if self.prepros_record['drop_col']:
                    temp=self.prepros_record['drop_col']
                temp.extend(cols)
                self.prepros_record['drop_col']=temp            

            float_cols = df.select_dtypes(include=['float']).columns
            df[float_cols] = df[float_cols].astype(int)
            df.to_csv(f"preprocess.csv",index=False)  
            records = df.to_dict("records")
            with open("preprocess_record.json", "w") as json_file:
                json.dump(self.prepros_record, json_file, indent=4) 
            return records
        except:
            return []
        
    def find(self,pridict_input):
        data = json.loads(pridict_input)
        df1=pd.DataFrame(list([data.values()]),columns=list(data.keys()))
        with open('preprocess_record.json', 'r') as file:
            preprocess_data = json.load(file)
        drop_col=preprocess_data['drop_col']
        onehot_encode_col=preprocess_data['onehot_encode']
        label_encode_col=preprocess_data['label_encode']
        #drop cols
        df1.drop(drop_col,axis=1,inplace=True)
        # one hot encode
        if self.onehot_encoded_status:
            input_onehot_encoded = onehot_encoder.transform(df1[onehot_encode_col])
            input_onehot_col= onehot_encoder.get_feature_names_out(onehot_encode_col)
            onehoted_df = pd.DataFrame(input_onehot_encoded.toarray(), columns=input_onehot_col)
            df1.drop(columns=onehot_encode_col, inplace=True)
            df1 = pd.concat([onehoted_df, df1], axis=1)
        #label encode
        if self.label_encoder_status:
            for col_name, encoder in self.label_encoders.items():
                if col_name in df1.columns:
                    df1[col_name] = encoder.transform(df1[col_name])
        #load pickle file
        print(df1)
        with open('model.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
        df1.drop(["math score"],axis=1,inplace=True)
        predict=loaded_model.predict(df1.sort_index(axis=1))
        print(predict)
        if False:
            pass
        else: 
            return predict