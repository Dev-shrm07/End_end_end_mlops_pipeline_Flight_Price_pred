import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
import os


class PredictPipeline:
    def __init__(self):
        model_path=os.path.join("artifacts","models","model.pkl")
        preprocessor_path=os.path.join('artifacts','models','preprocessor.pkl')
        self.model=load_object(file_path=model_path)
        self.preprocessor=load_object(file_path=preprocessor_path)

    def predict(self,features):
        try:
            data_scaled=self.preprocessor.transform(features)
            preds=self.model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)




