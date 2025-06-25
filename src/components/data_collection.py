import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def download_s3_file(bucket_name, s3_key, download_path):

    try:
        s3 = boto3.client('s3')
        
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_key)
        if 'Contents' not in response or all(obj['Key'] != s3_key for obj in response['Contents']):
            print(f"File '{s3_key}' not found in bucket '{bucket_name}'.")
            return False
       
        s3.download_file(bucket_name, s3_key, download_path)
        print(f"File '{s3_key}' downloaded to '{download_path}'.")
        return True
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False




def getData():
    bucket = "raws3e2eml"
    file_key = "data.csv"             
    local_path  = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data','raw','raw.csv')  

    return download_s3_file(bucket, file_key, local_path)
