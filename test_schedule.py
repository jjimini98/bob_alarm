import os
import logging
from slack_sdk.errors import SlackApiError
from slack_sdk.web import WebClient

client = WebClient(token="xoxb-1043508635344-7254887594864-BO0dRkbB65JNiEVICaUbdQFc")
logger = logging.getLogger(__name__)

# List scheduled messages using latest and oldest timestamps
def list_scheduled_messages(latest, oldest):
    try:
        # Call the chat.scheduledMessages.list method using the WebClient
        result = client.chat_scheduledMessages_list(
            latest= latest,
            oldest= oldest
        )

        # Print scheduled messages
        for message in result["scheduled_messages"]:
            logger.info(message)

    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))
    
    return result


if __name__ == "__main__": 
   print( list_scheduled_messages(1718964600,1718680200))



# deleted scheduled message

# import logging
# import os
# # Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError

# # # WebClient instantiates a client that can call API methods
# # # When using Bolt, you can use either `app.client` or the `client` passed to listeners.
# client = WebClient(token="xoxb-1043508635344-7254887594864-BO0dRkbB65JNiEVICaUbdQFc")
# logger = logging.getLogger(__name__)

# # # The ts of the message you want to delete
# # message_id = "Q078XLW4EQ0"
# # # ID of channel that the scheduled message was sent to
# channel_id = "C076U06K6EB"
# message_id = ["Q077UAHMK39", "Q07828EAXCN"]
# try:
#     # Call the chat.deleteScheduledMessage method using the built-in WebClient
#     result = client.chat_deleteScheduledMessage(
#         channel=channel_id,
#         scheduled_message_id="Q07828EAXCN"
#     )
#     # Log the result
#     logger.info(result)

# except SlackApiError as e:
#     logger.error(f"Error deleting scheduled message: {e}")