from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from Prediction import Prediction
from Modeltrain import Modeltrain
from Load_data import Load_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, etc.)
)

@app.get("/test")
def test():
    return "<h1>hellow test</h1>"

obj=Load_data()

@app.post("/file_upload")
async def file_upload(file: UploadFile= File(...)):
    status=await obj.save_file(file)
    return status
    
@app.get("/fetch_data")
async def fetch_data():
    res_data=obj.get_data()
    return res_data

code=Prediction()

@app.post("/preprocess")
async def preprocess(col: str = Form(...), prepros: str = Form(...)):
    pros_res=code.process(col, prepros)
    return pros_res

# model=Modeltrain()

# @app.post("/train")
# async def preprocess(col: str = Form(...), algorithm: str = Form(...), problem: str = Form(...)):
    
#     model_res=model.train_model(col,algorithm, problem)
#     return model_res


# @app.get("/fetch_pickle")
# async def fetch_picklefile():
#     model_res=model.get_picklefile()
#     return model_res
    
# @app.get("/json_input")
# async def fetch_jsoninput():
#     predict_res=code.get_json_input()
#     return predict_res


# @app.post("/predictions")
# async def preprocess(pridict_input: str= Form(...)):
#     predict_res=code.find(pridict_input)
#     return predict_res

if __name__ == '__name__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=True)