import boto3
from dotenv import load_dotenv
import pickle
import io

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


def upload_s3_file(bucket_name, s3_key, upload_path):
    try:
        s3 = boto3.client('s3')
        s3.upload_file(upload_path, bucket_name, s3_key)
        print(f"File '{upload_path}' uploaded to '{s3_key}' in bucket '{bucket_name}'.")
        return True
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return False


def load_pickle_from_s3(bucket_name, s3_key):
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=s3_key)
        obj = pickle.loads(response['Body'].read())
        print(f"Pickle object loaded from '{s3_key}' in bucket '{bucket_name}'.")
        return obj
    except Exception as e:
        print(f"Error loading pickle object: {str(e)}")
        return None
    
    
    
def save_pickle_to_s3(obj, bucket_name, s3_key):
    try:
        s3 = boto3.client('s3')
        pickle_buffer = io.BytesIO()
        pickle.dump(obj, pickle_buffer)
        pickle_buffer.seek(0)
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=pickle_buffer)
        print(f"Pickle object uploaded to '{s3_key}' in bucket '{bucket_name}'.")
        return True
    except Exception as e:
        print(f"Error uploading pickle object: {str(e)}")
        return False