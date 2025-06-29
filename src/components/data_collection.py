import sys
import os
path_to_add = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path_to_add)
from src.components.handles3 import download_s3_file


def getData():
    bucket = "raws3e2eml"
    file_key = "data.csv"             
    local_path  = os.path.join(path_to_add,'data','raw','raw.csv')  
    return download_s3_file(bucket, file_key, local_path)
