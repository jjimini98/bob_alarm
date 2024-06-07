import os
from dotenv import load_dotenv
load_dotenv(verbose=True)
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json 
import datetime
import logging
logger = logging.getLogger(__name__)

channel_id = os.getenv("CHANNEL_ID")
client = WebClient(token=os.environ.get("BOT_TOKEN"))

def calculate_datetime(date : str):
    # 현재 날짜를 구합니다.
    current_date = datetime.datetime.now().date()
    date_with_year = f"{current_date.year}/{date}"
    target_date = datetime.datetime.strptime(date_with_year, "%Y/%m/%d").date()
    date_difference = target_date - current_date

    return date_difference.days

def transform_menu(file : str):
    global lunch_menu 
    global dinner_menu
    lunch_menu = dict()
    dinner_menu = dict()

    with open(file, "r") as f: 
        file = json.load(f)

    for key,value in file.items():
        for k,v in value.items():
            if "점심" in k : 
                lunch_menu[key + ' ' + k] = v
            elif "저녁" in k : 
                dinner_menu[key + ' ' + k] = v

    return lunch_menu, dinner_menu


def alert_lunch(input_date : str):
    for d, m  in lunch_menu.items():
        if input_date in d: 
            num = calculate_datetime(input_date)
            reserve_date = datetime.date.today() + datetime.timedelta(days=num)
            # reserve_date = datetime.date.today()
            scheduled_time = datetime.time(hour=10, minute=00)
            schedule_timestamp = datetime.datetime.combine(reserve_date, scheduled_time).strftime('%s')

            try:
                # Call the chat.scheduleMessage method using the WebClient
                result = client.chat_scheduleMessage(
                    channel=channel_id,
                    text= "==============================\n"+ d+ "\n==============================\n" + m,
                    post_at=schedule_timestamp
                )
                # Log the result
                logger.info(result)

            except SlackApiError as e:
                logger.error("Error scheduling message: {}".format(e))

def alert_dinner(input_date : str):
    for d, m  in dinner_menu.items():
        if input_date in d: 
            num = calculate_datetime(input_date)
            reserve_date = datetime.date.today() + datetime.timedelta(days=num)
            # reserve_date = datetime.date.today()
            scheduled_time = datetime.time(hour=16, minute=00)
            schedule_timestamp = datetime.datetime.combine(reserve_date, scheduled_time).strftime('%s')

            try:
                # Call the chat.scheduleMessage method using the WebClient
                result = client.chat_scheduleMessage(
                    channel=channel_id,
                    text= "==============================\n"+ d+ "\n==============================\n" + m,
                    post_at=schedule_timestamp
                )
                # Log the result
                logger.info(result)

            except SlackApiError as e:
                logger.error("Error scheduling message: {}".format(e))

if __name__ == "__main__":

    filename = "test_result/test1.json"
    transform_menu(filename)
    alert_lunch("06/07")
    alert_dinner("o6/07")

    # print(calculate_datetime("06/07"))
    # print(transform_menu("test_result/test1.json"))

