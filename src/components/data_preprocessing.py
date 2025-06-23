import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
import stats
import os



@dataclass
class DataTransformationConfig:
    preprocessor_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'artifacts','models','preprocessor.pkl')
    processed_data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data','processed','processed_data.csv')
    

class DataPreprocssing:
    def __init__(self):
        self.preprocessor_file_path = DataTransformationConfig.preprocessor_file_path
        self.processed_data_file = DataTransformationConfig.processed_data_file
        

    
    def get_data_transformer_object(self, numerical_cols, categorical_cols):
        try:
            
            num_pipeline=Pipeline(steps=[
                ('scalar',StandardScaler())

            ])
            
            cat_pipeline=Pipeline(steps=[
            
            ("one_hot_encoder",OneHotEncoder()),
            ("scaler",StandardScaler(with_mean=False))
            
            ])

           

            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_cols),
                    ("cat_pipeline",cat_pipeline,categorical_cols)
                ]

            )
            return preprocessor
            

        except Exception as e:
            raise CustomException(e,sys)
        
        
    def preprocess_data(self):
        try:
            
            df = pd.read_csv(self.processed_data_file)
    
            
            target_column_name="price"
            X = df.drop(columns=[target_column_name])
            Y = df[target_column_name].values
            
            numerical_cols = [col for col in X.columns if df[col].dtype != 'object']
            cat_cols = [col for col in X.columns if df[col].dtype == 'object']
            
            logging.info(f"Numerical columns to be scaled are {" ".join(numerical_cols)}")
            logging.info(f"Categorical columns to be encoded are {" ".join(cat_cols)}")
            
            
            preprocessing_obj = self.get_data_transformer_object(numerical_cols=numerical_cols, categorical_cols=cat_cols)
            
            logging.info("Preprocessing object created")
            
            X_normalized = preprocessing_obj.fit_transform(X)

            save_object(

                file_path=self.preprocessor_file_path,
                obj=preprocessing_obj
            )
            
            logging.info("Preprocessor Saved")
            
            return X_normalized, Y



        except Exception as e:
            raise CustomException(e,sys)
