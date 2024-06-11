import os
from dotenv import load_dotenv
load_dotenv(verbose=True)
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from transform_menu import OCR
from datetime import datetime , timedelta
import datetime
import logging
import asyncio
logger = logging.getLogger(__name__)


class ConnectSlack:
    def __init__(self,image):
        self.channel_id = os.getenv("CHANNEL_ID")
        self.client = WebClient(token=os.environ.get("BOT_TOKEN"))
        self.ocr_result = OCR(image).necessary_date()
        # print(self.ocr_result)
        # print(self.min_diff, self.max_diff, self.ocr_result) # 실행 시간과 월요일 간 날짜 차이 


    async def alert(self, num, debug = False):
        today = datetime.datetime.today().date()
        two_days_later = today + timedelta(days=num)
        formatted_date = two_days_later.strftime('%m/%d')
        
        for diff , day in self.ocr_result.items():

            if num == diff :
                reserve_date = datetime.date.today() + datetime.timedelta(days=num)
                # reserve_date = datetime.date.today()

                for menu in day: 
                    for k in menu.keys():
                        menu_date = str(k)

                        if "점심" in menu_date: 
                            for v in menu.values():
                                menu_menu = str(v)
                            lunch = datetime.time(hour=18, minute=27)
                            lunch_timestamp = datetime.datetime.combine(reserve_date,lunch).strftime('%s')

                            lunch_result = self.client.chat_scheduleMessage(
                                    channel = self.channel_id,
                                    text = "========================" + "\n" + menu_date + "\n"+ "========================" + "\n" + menu_menu,
                                    post_at=lunch_timestamp
                                )
                            logger.info(lunch_result)

                        else: 
                            for v in menu.values():
                                menu_menu = str(v)
                            dinner = datetime.time (hour = 18 , minute= 29)
                            dinner_timestamp = datetime.datetime.combine(reserve_date,dinner).strftime('%s')

                            dinner_result = self.client.chat_scheduleMessage(
                                channel= self.channel_id,
                                text = "========================" + "\n"+ menu_date + "\n" "========================" + "\n" + menu_menu,
                                post_at= dinner_timestamp

                            )
                            logger.info(dinner_result)


if __name__ == "__main__":
    async def main():
        filename = "test_image/test.png"
        connect = ConnectSlack(filename)
        await connect.alert(6)
        await connect.alert(5)
        await connect.alert(4)
        await connect.alert(3)
        await connect.alert(2)

    asyncio.run(main())


