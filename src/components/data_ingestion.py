import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging
import stats
import os



@dataclass
class DataIngestionConfig:
    raw_data_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data','raw','raw.csv')
    processed_data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data','processed','processed_data.csv')
    

class DataIngestion:
    def __init__(self):
        self.raw_data_file_path = DataIngestionConfig.raw_data_file_path
        self.processed_data_file = DataIngestionConfig.processed_data_file
        

    def remove_outliers(self, df, method='iqr', columns=['price'], threshold=3):
        try:
            df_clean = df.copy()
            if columns is None:
                columns = df_clean.select_dtypes(include=[np.number]).columns.tolist()
            
            if method not in ['iqr', 'zscore']:
                raise ValueError("Method must be 'iqr' or 'zscore'")
            
            mask = pd.Series([True] * len(df_clean), index=df_clean.index)
            
            for col in columns:
                if col not in df_clean.columns:
                    print(f"Warning: Column '{col}' not found in DataFrame")
                    continue
                    
                if not pd.api.types.is_numeric_dtype(df_clean[col]):
                    print(f"Warning: Column '{col}' is not numeric, skipping")
                    continue
                
                if method == 'iqr':
                    
                    Q1 = df_clean[col].quantile(0.25)
                    Q3 = df_clean[col].quantile(0.75)
                    IQR = Q3 - Q1
                    
                
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    
                    column_mask = (df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)
                    mask = mask & column_mask
                    
                elif method == 'zscore':
                    
                    z_scores = np.abs(stats.zscore(df_clean[col].dropna()))
                
                    non_null_mask = df_clean[col].notna()
                    
                    
                    column_mask = pd.Series([True] * len(df_clean), index=df_clean.index)
        
                    column_mask.loc[non_null_mask] = z_scores <= threshold
                    
                
                    mask = mask & column_mask

            df_clean = df_clean[mask]
            logging.info(f"Rows removed: {df.shape[0] - df_clean.shape[0]} During outlier removal using {method} method")

            return df_clean
        
        except Exception as e:
            raise CustomException(e,sys)
    

        
    def ingest_data(self, outlier_method='iqr', outlier_threshold=3):
        try:
            
            df = pd.read_csv(self.raw_data_file_path)
            df.drop(columns=['Unnamed: 0','flight'],inplace=True)

            logging.info("Reading the raw data")
            
            df = df.dropna()
            logging.info("Removing nulls and missing values without any imputatuion since there are almost 0")

            logging.info(f"Removing outliers on the data using {outlier_method} method")
            df_clean = self.remove_outliers(df, method=outlier_method, threshold=outlier_threshold)
            
            df_clean.to_csv(self.processed_data_file,index=False)
            
            os.remove(self.raw_data_file_path)
            



        except Exception as e:
            raise CustomException(e,sys)
