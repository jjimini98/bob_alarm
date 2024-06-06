import os 
import requests
import uuid
import time 
import json
from dotenv import load_dotenv
from tqdm import tqdm 
from collections import defaultdict
load_dotenv(verbose=True) 

class OCR:
    def __init__(self):
        self.API  = os.getenv("INVOKE_URL")
        self.SECRETKEY = os.getenv("SECERT_KEY")

    def request_img(self, img : str) -> str: 
        """
        clova ocr API 요청 보내기 
        """
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
        'X-OCR-SECRET': self.SECRETKEY
        }

        response = requests.request("POST", self.API, headers=headers, data = payload, files = files)

        return response.text        


    def extract_response(self,result : str):
        result = json.loads(result)  #str을 dict로 변경 
        extract = dict()
        ocr_result = result.get("images")[0]
        daily_bob = ocr_result.get("fields")
        for daily in daily_bob:
            text = daily.get("inferText")
            extract[daily.get("name")] = text 

        return extract
    

    def split_data(self,extract_data : dict):
        weekly_menu = defaultdict(dict)

        for k,v in extract_data.items():
            split_dict = dict()
            if "그린샐러드&드레싱\n" in v : 
                split_dict["점심"] = v.split("그린샐러드&드레싱\n")[0]
                split_dict["저녁"] = v.split("그린샐러드&드레싱\n")[1]
            elif "바나나\n" in v:
                split_dict["점심"] = v.split("바나나\n")[0]
                split_dict["저녁"] = v.split("바나나\n")[1]
            weekly_menu[k] = split_dict
        

        return weekly_menu    

    def convert_json(self, menu : dict , img_name : str) : 
        with open(f'./test_result/{img_name}.json','w') as f:
                json.dump(menu, f, ensure_ascii=False, indent=4)
        
        print(f"==================={img_name} 변환 완료===================")



if __name__ == "__main__":
    # 여기서 이미지를 직접 넣어준다 
    ocr = OCR()
    for img in tqdm(os.listdir("test_image")):
        if img != ".DS_Store":
            imgname = img.split(".")[0]
            res = ocr.request_img(f"test_image/{imgname}.JPG")
            ees = ocr.extract_response(res)
            menu = ocr.split_data(ees)
            ocr.convert_json(menu, imgname)


