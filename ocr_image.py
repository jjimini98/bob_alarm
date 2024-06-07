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
    def __init__(self,img):
        self.image = img
        self.API  = os.getenv("INVOKE_URL")
        self.SECRETKEY = os.getenv("SECERT_KEY")

    def request_image(self) -> str: 
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
        ('file', open(self.image,'rb'))
        ]
        headers = {
        'X-OCR-SECRET': self.SECRETKEY
        }

        response = requests.request("POST", self.API, headers=headers, data = payload, files = files)

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
    

    def convert_datetime(self,datetime):
        """
        날짜의 달과 일을 항상 두자리 수로 맞춰줌
        """
        month, date = map(int,datetime.split("/"))
        if month < 10 and date > 10:
            return "0" + str(month) + "/" + str(date)
        elif month < 10 and date < 10: 
            return "0" + str(month) + "/" + "0" + str(date)
        elif month > 10 and date > 10:
            return str(month) + "/" + str(date)
        else: 
            return str(month) + "/" + "0" +str(date)
        


    def split_lunch_dinner(self):
        """
        기준을 가지고 요일별 점심,저녁 메뉴를 나눈다.
        """
        total_menu = self.transform_result()
        weekly_menu = defaultdict(dict)

        for day , menu in total_menu.items():
            daydict = dict()
            datetime = self.convert_month(menu[:4])
            day = datetime + " " + day
            if "그린샐러드&드레싱\n" in menu : 
                lunch = menu.split("그린샐러드&드레싱\n")[0]
                daydict[day+" 점심"] = lunch[9:]
                daydict[day+" 저녁"] = menu.split("그린샐러드&드레싱\n")[1]
            elif "바나나\n" in menu:
                lunch = menu.split("바나나\n")[0]
                daydict[day+" 점심"] = lunch[9:]
                daydict[day+" 저녁"] = menu.split("바나나\n")[1]
            else:
                daydict[day+" 점심"] = "없음"
                daydict[day+" 저녁"] = "없음"
            weekly_menu[day] = daydict
        
        return weekly_menu    


if __name__ == "__main__":
    filename = "test_image/test1.JPG"
    ocr = OCR(filename)
    print(ocr.split_lunch_dinner())

