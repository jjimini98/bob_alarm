import os 
import requests
import uuid
import time 
import json
from dotenv import load_dotenv
from tqdm import tqdm 
from collections import defaultdict
from datetime import datetime
import pymongo
load_dotenv(verbose=True) 

"""
clova OCR API로 이미지를 읽어와서 json 파일로 저장합니다.

"""

class Request:
    def __init__(self,img):
        self.image = img
        self.API  = os.getenv("ADD_INVOKE_URL")
        self.SECRETKEY = os.getenv("ADD_SECERT_KEY")

    def request_image(self) -> str: 
        """
        clova ocr API 요청 보내기 
        """
        request_json = {
            'images': [
                {
                    'format': 'png',
                    'name': 'test'
                }
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V1',
            'timestamp': int(round(time.time() * 1000))
        }

        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        files = [
        ('file', open(self.image,'rb'))
        ]
        headers = {
        'X-OCR-SECRET': self.SECRETKEY
        }

        response = requests.request("POST", self.API, headers=headers, data = payload, files = files)
        # print(response.text)
        return response.text        

    def transform_result(self):
        """
        인식된 결과를 {요일 : 메뉴} 의 형태로 리턴해준다. 
        """
        # str -> dict 
        result = json.loads(self.request_image()) 
        weekly_menu = dict()

        extract_result = result['images'][0]["fields"]
        for result in extract_result:
            weekday = result['name']
            menu = result['inferText']
            weekly_menu[weekday] = menu

        return weekly_menu
    

    def convert_json(self,filename):
        with open(f"test_result/{filename}.json", "w") as f: 
            json.dump(self.transform_result(), f, ensure_ascii=False, indent=4)
        return "=================CONVERT JSON COMPLETE================="


    def load_db(self,filenumber):
        conn = pymongo.MongoClient(host= "localhost", port=27017)
        db = conn["menus"]
        col = db["menu"]
        with open(f"test_result/test{filenumber}.json", "r") as f: 
            json_data = json.load(f)
            for _,v in json_data.items():
                new_json = {} 
                v = v.split("\n")
                new_json[v[0]] = ' '.join(v[1:])
                x = col.insert_one(new_json)
                print(x)
            
    


if __name__ == "__main__":
    # 테스트 이미지 수 만큼 반복문 돌리기 
        ocr = Request(f"test_image/test21.png")
        ocr.convert_json(f"test21")
        ocr.load_db("21")
    
