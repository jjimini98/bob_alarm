import os
from dotenv import load_dotenv
load_dotenv(verbose=True)
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from transform_menu import Transformation
from datetime import datetime , timedelta, time
# import datetime
import logging
import asyncio
logger = logging.getLogger(__name__)


class ConnectSlack:
    def __init__(self,file):
        self.channel_id = os.getenv("CHANNEL_ID")
        self.channel_id = os.getenv("TEST_CHANNEL_ID")
        self.client = WebClient(token=os.environ.get("BOT_TOKEN"))
        self.ocr_result = Transformation(file).split_lunch_dinner()


    def search_date(self, spec_date):
        result = [] 
        today = datetime.today().date() 
        today_year = str(datetime.today().year)
        for day , menu in self.ocr_result.items():
            if spec_date in day: 
                date = day.split(" ")[0]
                date = today_year + "/" + date
                date = datetime.strptime(date, "%Y/%m/%d").date()
                diff = (date - today).days
                result.append({day:menu})
 
        return diff, result 
            
    def alert(self,spec_date):
        diff, today_menu = self.search_date(spec_date)
        reserve_date = datetime.today() + timedelta(days=diff) #diff로 바꿔야함 
        for today in today_menu:
            for date, menu in today.items(): 

                if "점심" in date:
                    text = "*:선글라스거북:"  + date +  ":선글라스거북:*" + "\n\n" + menu
                    reserve_time = time(hour=8, minute=00)
                    timestamp = datetime.combine(reserve_date,reserve_time).strftime('%s')
                else: 
                    text = "*:선글라스거북:"  + date +  ":선글라스거북:*" + "\n\n" + menu
                    reserve_time = time(hour=8, minute=1)
                    timestamp = datetime.combine(reserve_date,reserve_time).strftime('%s')

                result = self.client.chat_scheduleMessage(
                            channel = self.channel_id,
                            text = text,
                            post_at=timestamp
                                        )

        print(result)

    def alert_lunch_time(self,spec_date):
        diff, _ = self.search_date(spec_date)
        reserve_date = datetime.today() + timedelta(days=diff) #diff로 바꿔야함 
        text = "*:파티댄스: "  + "해피 점심시간" +  " :파티댄스:*" 
        reserve_time = time(hour=12, minute=9)
        timestamp = datetime.combine(reserve_date,reserve_time).strftime('%s')
        result = self.client.chat_scheduleMessage(
                            channel = self.channel_id,
                            text = text,
                            post_at=timestamp
                                        )
        print(result)

    def alert_dinner_time(self,spec_date):
        diff, _ = self.search_date(spec_date)
        reserve_date = datetime.today() + timedelta(days=diff) #diff로 바꿔야함 
        text = "*:파티댄스:"  + "해피 저녁시간" +  ":파티댄스:*" 
        reserve_time = time(hour=17, minute=59)
        timestamp = datetime.combine(reserve_date,reserve_time).strftime('%s')
        result = self.client.chat_scheduleMessage(
                            channel = self.channel_id,
                            text = text,
                            post_at=timestamp
                                        )
        print(result)


    



if __name__ == "__main__":
    conn = ConnectSlack("test18")
    
    conn.alert("06/19")
    conn.alert_lunch_time("06/19")
    conn.alert_dinner_time("06/19")

    conn.alert("06/20")
    conn.alert_lunch_time("06/20")
    conn.alert_dinner_time("06/20")

    conn.alert("06/21")
    conn.alert_lunch_time("06/21")
    conn.alert_dinner_time("06/21")
