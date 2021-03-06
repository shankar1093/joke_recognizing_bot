from slackclient import SlackClient
import json
import nltk
import time
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import pickle

slack_token = "xoxp-54759295125-54769515010-163829435204-f3df9fef04159dae5d24a274a187432d"

def word_feats(words):
    return dict([(word, True) for word in words])
 

def create_corpus(slack_token,user):
    """ retrieve messages shared by nick in order to create corpus
        Args:
            slack_token: token used to communicate with API
        Returns:
            A value between 0 and 1 signfying humor quotient
"""
    sc = SlackClient(slack_token)
    users={"nick":"U1LN41FML", "shankar":"U1LNMF50A", "brad":"U1LM5NTU3", "streger":"U1LNTHZ3R"}
    l =sc.api_call(
        "channels.history",
        channel ="C1LNMF6JW",
        latest=time.time())

    _corpus = []
    for i in range(len(l['messages'])):
        if 'user'in l['messages'][i]:
            if l['messages'][i]['user'] == users[user]:
                _corpus.append(l['messages'][i]['text'])
    return _corpus


def judge_statement(statements):
    """ Returns a sentiment value to help plebians understand the great nick

        create a corpus of the latest messages shared by nick,
        assign a sentiment to each statement, if the resulting average is generally negative imply joke

        Args:
            corpus : a list of recently shared messages by nick in #general
        Returns:
            A value between 0 and 1 signfying humor quotient
    """
    f = open('my_classifier.pickle', 'rb')
    cl = pickle.load(f)
    f.close()
    pos = 0
    neg = 0
    for i in statements:
    	if str(cl.classify(word_feats(i))) == "neg":
    		neg+=1
    	else:
    		pos+=1

    response = float(pos)/float(neg) 		
    if response<0.5:
        percent = 100-response*100
        slack_client.api_call("chat.postMessage", channel=channel,
                      text=str(percent)+"% joke", as_user=True)

    else:
        percent = response*100-50
        slack_client.api_call("chat.postMessage", channel=channel,
                      text=str(percent)+"% not a joke", as_user=True)


# starterbot's ID as an environment variable
BOT_ID = "U4ULT8A3G"
# constants
AT_BOT = "<@" + BOT_ID + ">"
nick_translation = "translate nick"
brad_translation = "translate brad"
streger_translation = "translate streger"
shankar_translation = "translate shankar"

slack_client = SlackClient(slack_token)



def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    peeps = {"translate nick":"nick", "translate brad":"brad", "translate streger":"streger", "translate shankar":"shankar"}
    
    response = "Not sure what you mean. Use the *" + nick_translation + ", "+brad_translation+", "+streger_translation+", "+shankar_translation+\
               "* command with numbers, delimited by spaces."

    if command in peeps:
        response = judge_statement(create_corpus(slack_token,peeps[command]))
    else:
        slack_client.api_call("chat.postMessage", channel=channel,
                      text=response, as_user=True)



def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

# print sc.api_call("channels.list")

#U1LNMF50A <- shankar
#U1LM5NTU3 <- brad
#U1LN41FML <- NICK
#random <- random 
# C1LNMF6JW<-general