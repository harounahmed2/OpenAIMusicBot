import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from dotenv import load_dotenv
import openai
import pprint as pp
from helpers import * # import helpers to manage logic of session - this file is main control
from music import MusicBot # import MusicBot Object for initial display

# load env variables into python program
load_dotenv()


#credentials for auth come from backend Slack account and app auth- exported in py venv
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET= os.environ.get('SLACK_SIGNING_SECRET')
openai.api_key = os.environ.get('OPENAI_API_KEY')



#activate Slack credentials from Source, raise RuntimeError if absent
if SLACK_BOT_TOKEN is None or SLACK_SIGNING_SECRET is None:
    raise RuntimeError("Error: Unable to find environment keys. Exiting.")


#globals
# app = Flask(__name__) #Flask app to run server
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

#delete bot messages from previous iteration for clean demo
delete_bot_convo_messages(app)

def start_onboarding(user_id: str, channel: str, say):
    """initiate onboarding message- Using bot class from expense
        for clean initial markdown display
    """
    # Create a new welcome message.
    Bot = MusicBot(channel)
    # Get the onboarding message payload
    message = Bot.get_welcomeMessage_payload()
    # Post the onboarding message in Slack
    say(message)


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your MusicBot's Home_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This app uses OpenAI powered API's to help you discover and listen to music!"
            }
          },
        ]
      }
    )
  
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")


@app.event("message")
def handle_message(message, say):
    """Handle user messaging and fork logic based on user option selection".
    """
    channel_id = message.get("channel")
    user_id = message.get("user")
    text = message.get("text")
    
    #hard coded userID for Haroun to filter out Bot response and avoid infinite loop- fine for single user
    if user_id == 'U010PEBLK89':
        
        if text and text.lower() == "start": #initial message- display onboarding
            return start_onboarding(user_id, channel_id, say)
        
        elif text and "time machine" in text.lower(): #user wants to use time functionality 
            gpt_input = time_method(text, say)
        elif text and "genre" in text.lower(): #user wants to discover by genre
            gpt_input = genre_method(text, say)
        elif text and "global" in text.lower(): #user wants to discover by region
            gpt_input = global_method(text, say)
        elif text and "popular" in text.lower(): #user wants popular music
            gpt_input = popular_method(text, say)
        elif text and "surprise" in text.lower(): #user wants random function from above
            gpt_input = surprise_method(text, say)


        #Catchall for unprocessable input
        else:
            response = "Sorry, we are unable to adequately parse your response at this time. Please use keywords from main menu."
            say(response)
            return
        
        #Take dynamic response from GPT3 and output response to slackbot for rendering
        answer = get_response(gpt_input)
        answer = answer.replace('?','') # get rid of GPT ?, doesn't help to know that it's guessing on output even with temp
        say(answer) 

# Main loop- running flask server
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))