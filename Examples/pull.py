import sys
import time
import configparser
from slackclient import SlackClient



'''
Get values from config file: slack_token, slack_channel, test_username

Essentially all of this code from this method is from Chris. Thanks!
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


def main():
    slack_token, slack_channel, test_username = get_config_info()

    '''
    What we came for
    '''
    sc = SlackClient(slack_token)
    print(sc.rtm_connect()) # If connected, prints True
    while True:
        raw_data = sc.rtm_read() # Retuns a dictionary in a list
        print(raw_data)
        time.sleep(.5)


if __name__ == '__main__':
    main()