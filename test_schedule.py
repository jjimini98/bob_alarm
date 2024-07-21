import os
import logging
from slack_sdk.errors import SlackApiError
from slack_sdk.web import WebClient

client = WebClient(token="xoxb-1043508635344-7254887594864-BO0dRkbB65JNiEVICaUbdQFc")
logger = logging.getLogger(__name__)
message_list = [] 
# List scheduled messages using latest and oldest timestamps
def list_scheduled_messages(latest, oldest):
    try:
        # Call the chat.scheduledMessages.list method using the WebClient
        result = client.chat_scheduledMessages_list(
            latest=latest, 
            oldest=oldest
        )
        print(result)
        # Print scheduled messages
        for message in result["scheduled_messages"]:
            message_list.append(message.get("id"))

        return message_list
    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))



scheduled  = list_scheduled_messages(latest="1718975851", oldest="1718716651")
print(scheduled)



