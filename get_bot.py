import os
from slackclient import SlackClient


BOT_NAME = 'translator'
slack_token = "xoxp-54759295125-54769515010-163829435204-f3df9fef04159dae5d24a274a187432d"
slack_client = SlackClient(slack_token)


if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)