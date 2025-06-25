import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.request_model import InputData
from src.components.predict_pipeline import PredictPipeline
import pandas as pd
import uvicorn



predict_pipeline = PredictPipeline()

app = FastAPI()


origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def getHome():
    return {"Welcome"}


@app.post("/api/price_prediction")
async def getPricePrediction(input_data:InputData):
    try:
        df = df = pd.DataFrame([input_data.dict()])
        df.rename(columns={'Class':'class'},inplace=True)
        cols = ['airline','source_city','departure_time','stops','arrival_time','destination_city','class','duration','days_left']
        df = df[cols]
        results = predict_pipeline.predict(df)
        return {"price":results[0]}
    except Exception as e:
        raise HTTPException(500, f"Interna server error {str(e)}")
    
    
    
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port = 8000)