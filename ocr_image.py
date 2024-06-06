import os 
import requests
import uuid
import time 
import json
from dotenv import load_dotenv
from tqdm import tqdm 
load_dotenv(verbose=True) 


API  = os.getenv("INVOKE_URL")
SECRETKEY = os.getenv("SECERT_KEY")


def request_ocr(img : str): 
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'test'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V1',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
    ('file', open(img,'rb'))
    ]
    headers = {
    'X-OCR-SECRET': SECRETKEY
    }

    response = requests.request("POST", API, headers=headers, data = payload, files = files)

    return response.text 

def extract_json():
    for img in tqdm(os.listdir("test_image")):
        if img != ".DS_Store":
            img_name = img.split(".")[0]
            img_path = f"test_image/{img}"
            result = request_ocr(img_path) 
            time.sleep(1) #1분 30초 정도 소요됨
            with open(f'./test_result/{img_name}.json','w') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == "__main__": 
    extract_json()