import json
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime
load_dotenv(verbose=True) 
class Transformation:
    def __init__(self,file):
        with open(f"test_result/{file}.json", "r") as f:
            self.data = json.load(f)

    def convert_datetime(self,datetime):
        """
        날짜의 달과 일을 항상 두자리 수로 맞춰줌
        """
        month, date = map(int,datetime.split("/"))
        if month < 10 and date >= 10:
            return "0" + str(month) + "/" + str(date)
        elif month < 10 and date < 10: 
            return "0" + str(month) + "/" + "0" + str(date)
        elif month >= 10 and date >= 10:
            return str(month) + "/" + str(date)
        else: 
            return str(month) + "/" + "0" +str(date)
        
    def split_lunch_dinner(self):
        """
        기준을 가지고 요일별 점심,저녁 메뉴를 나눈다.
        """
        total_menu = self.data
        daydict = dict()

        for day , menu in total_menu.items():
            datetime = self.convert_datetime(menu[:4])
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
            # weekly_menu[day] = daydict
        
        return daydict    




if __name__ == "__main__":
    trans = Transformation(file="test20")
    print(trans.split_lunch_dinner())

