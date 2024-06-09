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
            
    def alert_lunch(self,spec_date):
        diff, today_menu = self.search_date(spec_date)
        reserve_date = datetime.today() + timedelta(days=diff)
        for today in today_menu:
            for date, menu in today.items():
                if "점심" in date: 
                    text = "========================" + "\n" + date + "\n"+ "========================" + "\n" + menu
                    lunch = time(hour=10, minute=00)
                    lunch_timestamp = datetime.combine(reserve_date,lunch).strftime('%s')

                    lunch_result = self.client.chat_scheduleMessage(
                            channel = self.channel_id,
                            text = text,
                            post_at=lunch_timestamp
                                        )
                    logger.info(lunch_result)
        print( "======================== " + spec_date + " lunch reserved"+ "========================")

        
    def alert_dinner(self,spec_date):
        diff, today_menu = self.search_date(spec_date)
        reserve_date = datetime.today() + timedelta(days=diff)
        for today in today_menu:
            for date, menu in today.items():
                if "저녁" in date: 
                    text = "========================" + "\n" + date + "\n"+ "========================" + "\n" + menu

                    dinner = time(hour=16, minute=00)
                    dinner_timestamp = datetime.combine(reserve_date,dinner).strftime('%s')

                    dinner_result = self.client.chat_scheduleMessage(
                            channel = self.channel_id,
                            text = text,
                            post_at=dinner_timestamp
                                        )
                    logger.info(dinner_result)
        print( "======================== " + spec_date + " dinner reserved"+ "========================")




if __name__ == "__main__":
    conn = ConnectSlack("test")
    conn.alert_lunch("06/10")
    conn.alert_dinner("06/10")

    conn.alert_lunch("06/11")
    conn.alert_dinner("06/11")

    conn.alert_lunch("06/12")
    conn.alert_dinner("06/12")

    conn.alert_lunch("06/13")
    conn.alert_dinner("06/13")

    conn.alert_lunch("06/14")
    conn.alert_dinner("06/14")
