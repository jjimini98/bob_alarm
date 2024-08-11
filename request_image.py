import os 
import requests
import uuid
import time 
import json
from dotenv import load_dotenv
import pymongo
load_dotenv(verbose=True)

"""
clova OCR API로 이미지를 읽어와서 json 파일로 저장합니다.

"""

class Request:
    def __init__(self,img):
        self.image = img
        self.API  = os.getenv("INVOKE_URL")
        self.SECRETKEY = os.getenv("SECERT_KEY")

    def request_image(self) -> str:
        """
        clova ocr API 요청 보내고, str 의 형태로 결과를 받는다.
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
        return response.text



    def refine_data(self,text : str) -> dict:
        """
        response.text로 받은 문자열을 json 형식으로 변경
        {요일 : inferText} 의 형태로 반환

        """
        weekly_menu = dict()
        response = json.loads(text)

        for field in response['images'][0]["fields"]:
            weekday = field['name']
            menu = field.get("inferText")

            weekly_menu[weekday] = menu

        return weekly_menu

    def convert_json(self,refine_dict : dict) :
        """
        딕셔너리를 넣으면 정해진 파일 이름으로 json 파일을 만들어 준다.
        """
        with open(f"test_result/{filename}.json", 'w') as f:
            json.dump(refine_dict,f,ensure_ascii=False, indent=4)
        print("=================CONVERT JSON COMPLETE=================")

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
        filename = "test26"
        ocr = Request(f"test_image/{filename}.png")
        result = ocr.request_image()
        refine_dict = ocr.refine_data(result)
        ocr.convert_json(refine_dict)


            

    
