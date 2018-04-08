from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from slackclient import SlackClient
import logging
import sys


def open_gsheet(gsheet_credentials):
    client = gspread.authorize(gsheet_credentials)
    activated_sheet = client.open("Birthdays_test").sheet1
    return activated_sheet

def validate_column_names(activated_sheet):
    row_values = activated_sheet.row_values(1)
    logging.debug("ROW_VALUES_TYPE:\n" + str(type(row_values)))
    logging.debug("ROW_VALUES:\n" + str(row_values))
    if not "full name ENG" in row_values:
        logging.error("'full name ENG_1' header is not in the google spreadsheet")
        sys.exit()
    if not "Date" in row_values:
        logging.error("'Date' header is not in the google spreadsheet")
        sys.exit()
        logging.error("Header 'Date_1' is not in the google spreadsheet")


def get_slack_user_names(slack_client):
    user_profiles = slack_client.api_call("users.list")["members"]
    logging.debug("user_profile:\n" + json.dumps(user_profiles, indent = 2))
    slack_users = {}
    for user in user_profiles:
        if not user["deleted"]:
            name = user["real_name"].lower()
            id = user["id"]
            slack_users[name] = id
    logging.debug("slack_users:\n" + json.dumps(slack_users, indent = 2))
    return slack_users


def get_gsheet_values(activated_sheet):
    gsheet_data = activated_sheet.get_all_records()
    logging.debug(gsheet_data)
    return gsheet_data


# Google spreadsheet needs to have a header for the column with full user names
def get_gspread_users(gsheet_data):
    current_date = date.today().strftime("%-d-%b")
    print('CURRENT DATE')
    print(current_date)
    gsheet_users = []
    for user in gsheet_data:
            if user['Date'] == current_date:
                gsheet_users.append(user['full name ENG'].lower())
    logging.debug("gsheet_users:\n" + str(gsheet_users))
    return gsheet_users


'''def post_message(slack_users, gsheet_users, slack_client):
    for user in slack_users:
        for member in gsheet_users:
            if user == member:
                slack_client.api_call("chat.postMessage",
                            channel=slack_users[user],
                            text="new message! - 4")
                slack_client.api_call("chat.postMessage",
                            channel="#general",
                            text="post to #general! - 4") '''


'''def post_message(slack_users, gsheet_users, slack_client):
    for member in gsheet_users:
        response = slack_client.api_call("chat.postMessage",
                                         channel=slack_users[member],
                                         text="Happy Bday, " + member)
        if not response["ok"]:
            slack_client.api_call("chat.postMessage",
                                  channel="#general",
                                  text="Say Happy Bday to " + member + "!")
        else:
            logging.warning(member + " doesn't exist in Slack")
            print()'''

def post_message(slack_users, gsheet_users, slack_client):
    for member in gsheet_users:
        try:
            slack_client.api_call("chat.postMessage",
                                             channel=slack_users[member],
                                             text="Happy Bday_2, " + member)
            logging.info("Bday notification has been personally sent to " + member )
        except KeyError as err:
            logging.warning("KeyError: " + str(err) + " does not exist in Slack")
        else:
            slack_client.api_call("chat.postMessage",
                                  channel="#general",
                                  text="Say Happy Bday_2 to " + member + "!")
            logging.info("Bday notification has been sent to "
                         + member + "in general channel")


def main():
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    JSON_FILE = '/home/yulia/python_projects/MyProject-d27a72192381.json'
    gsheet_credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)

    activated_sheet = open_gsheet(gsheet_credentials)
    validate_column_names(activated_sheet)
    slack_users = get_slack_user_names(slack_client)
    gsheet_data = get_gsheet_values(activated_sheet)
    gsheet_users = get_gspread_users(gsheet_data)
    post_message(slack_users, gsheet_users, slack_client)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    main()
