from datetime import date
from datetime import datetime
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


def validate_gsheet_headers(activated_sheet):
    gsheet_headers = activated_sheet.row_values(1)
    #logging.debug("gsheet_header:\n" + str(gsheet_headers))
    mandatory_gsheet_headers = ["full name ENG", "Date"]
    for header in mandatory_gsheet_headers:
        try:
            if header not in gsheet_headers:
                raise Exception(header + " header is not on the spreadsheet")
        except Exception as err:
            logging.error(err)
            sys.exit(err)


def get_gsheet_values(activated_sheet):
    gsheet_data = activated_sheet.get_all_records()
    #logging.debug(gsheet_data)
    return gsheet_data


def get_gsheet_users(gsheet_data):
    gsheet_users = []
    for user in gsheet_data:
        if user["full name ENG"] != "" and user["full name ENG"] != " ":
            sub_gsheet_users = {}
            name = user["full name ENG"]
            date = user["Date"]
            sub_gsheet_users["name"] = name
            sub_gsheet_users["date"] = date
            gsheet_users.append(sub_gsheet_users)
    #logging.debug("GSHEET_USERS: \n" + str(gsheet_users))
    return gsheet_users


def validate_gsheet_date(gsheet_users):
    for user in gsheet_users:
        try:
            datetime.strptime(user["date"], "%d-%b")
        except ValueError as err:
            logging.warning(user["name"] + ": date of birth format is incorrect; " + str(err))


def get_slack_users(slack_client):
    user_profiles = slack_client.api_call("users.list")["members"]
    #logging.debug("user_profile:\n" + json.dumps(user_profiles, indent = 2))
    slack_users = {}
    for user in user_profiles:
        if user["id"] != "USLACKBOT" and not user["deleted"] and not user["is_bot"]:
            name = user["real_name"].lower()
            id = user["id"]
            slack_users[name] = id
    #logging.debug("slack_users:\n" + str(slack_users))
    return slack_users


def post_slack_message(slack_users, gsheet_users, slack_client):
    current_date = date.today().strftime("%-d-%b")
    for user in gsheet_users:
        if user["date"] == current_date:
            try:
                slack_client.api_call("chat.postMessage",
                                      channel=slack_users[user["name"].lower()],
                                      text="Happy Bday_3, " + user["name"])
                logging.info("Bday notification has been personally sent to " + user["name"])
            except KeyError as err:
                logging.warning("KeyError: " + str(err) + " does not exist in Slack")
            else:
                slack_client.api_call("chat.postMessage",
                                      channel="#general",
                                      text="Say Happy Bday_3 to " + user["name"] + "!")
                logging.info("Bday notification has been sent to "
                             + user["name"] + " in general channel")


def main():
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    JSON_FILE = '/home/yulia/python_projects/MyProject-d27a72192381.json'
    gsheet_credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)

    activated_sheet = open_gsheet(gsheet_credentials)
    validate_gsheet_headers(activated_sheet)
    gsheet_data = get_gsheet_values(activated_sheet)
    gsheet_users = get_gsheet_users(gsheet_data)
    validate_gsheet_date(gsheet_users)
    slack_users = get_slack_users(slack_client)
    post_slack_message(slack_users, gsheet_users, slack_client)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    main()
