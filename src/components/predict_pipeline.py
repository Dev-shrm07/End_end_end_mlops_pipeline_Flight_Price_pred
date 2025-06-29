import sys
import pandas as pd
from src.exception import CustomException
import os
path_to_add = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path_to_add)
from src.components.handles3 import load_pickle_from_s3


class PredictPipeline:
    def __init__(self):
        model_path = "models/model.pkl"
        preprocessor_path = 'models/preprocessor.pkl'
        bucket_name = "raws3e2eml"
        self.model=load_pickle_from_s3(bucket_name=bucket_name, s3_key=model_path)
        self.preprocessor=load_pickle_from_s3(bucket_name=bucket_name, s3_key=preprocessor_path)

    def predict(self,features):
        try:
            data_scaled=self.preprocessor.transform(features)
            preds=self.model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)




