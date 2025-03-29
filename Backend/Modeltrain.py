import json
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,accuracy_score
import pickle
import os

from Preprocess import Preprocess

class Modeltrain():
    def __init__(self):
        pass

    def train_model(self,col,algorthm,problem):
        col_dict=json.loads(col)
        col=[key for key, value in col_dict.items() if value]
        # print(col, algorthm, problem)

        try:
            # file=os.listdir('Preprocess')
            df = pd.read_csv('preprocess.csv')
            # df.drop("Unnamed: 0",axis=1,inplace=True)
            y=df.pop(col[0])
            X=df.sort_index(axis=1)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            models = {
                'logistic_regression': LogisticRegression(max_iter=200),
                'random_forest': RandomForestClassifier(),
                'Support Vector Classifier': SVC(),
                'decision_tree': DecisionTreeClassifier(criterion='entropy', random_state=5)
            }
            r2=''
            for name, model in models.items():
                if name==algorthm:
                    model.fit(X_train,y_train)
                    y_pred = model.predict(X_test)
                    with open('model.pkl', 'wb') as file:
                        pickle.dump(model, file)
            if problem == "regression":
                r2 = r2_score(y_test, y_pred)
                return {"r2_score":r2}
            else:
                accuracy = accuracy_score(y_test, y_pred)
                return {"accuracy":accuracy}
        except:
            return {"message":"model error"}
        
    def get_picklefile(self,):
        try:
            file_path = os.path.join("model", "model.pkl")
            return {"message":"success"}
        except:
            return {"message":"fail"}
        
        