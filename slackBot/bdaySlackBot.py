from datetime import date
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from slackclient import SlackClient
import logging
import sys


def open_gsheet(gsheet_credentials):
    """
Getting access to sheet1 of "Birthdays_test" google spreadsheet

    :param gsheet_credentials: google spreadsheet credentials from json file
    :type gsheet_credentials: instance of oauth2client.service_account.ServiceAccountCredentials
    :return activated_sheet: accessed sheet1 of "Birthdays_test" google spreadsheet
    :rtype activated_sheet: instance of gspread.v4.models.Worksheet
    """
    client = gspread.authorize(gsheet_credentials)
    activated_sheet = client.open("Birthdays_test").sheet1
    return activated_sheet


def validate_gsheet_headers(activated_sheet):
    """
Validating "full name ENG" (contains employee's full name) and "Date" (contains employee's DOB) headers of the sheet.
In case any of the headers is spelt incorrectly, the script raises an exception and exits.

    :param activated_sheet: accessed sheet1 of "Birthdays_test" google spreadsheet
    :type activated_sheet: instance of gspread.v4.models.Worksheet
    """
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
    """
Getting the content of sheet1

    :param activated_sheet: accessed sheet1 of "Birthdays_test" google spreadsheet
    :type activated_sheet: instance of gspread.v4.models.Worksheet
    :return gsheet_data: the content of sheet1
    :rtype gsheet_data: list of dictionaries
    """
    gsheet_data = activated_sheet.get_all_records()
    #logging.debug(gsheet_data)
    return gsheet_data


def get_gsheet_users(gsheet_data):
    """
Getting a list of dictionaries containing user's full names and user's DOBs from sheet1

    :param gsheet_data: the content of sheet1
    :type gsheet_data: list of dictionaries
    :return gsheet_users: contains user's full names and user's DOBs
    :rtype gsheet_users: list of dictionaries
    """
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
    """
Checking if DOB is of a correct format. In case it is not, a warning is logged.

    :param gsheet_users: contains user's full names and user's DOBs
    :type gsheet_users: list of dictionaries
    """
    for user in gsheet_users:
        try:
            datetime.strptime(user["date"], "%d-%b")
        except ValueError as err:
            logging.warning(user["name"] + ": date of birth format is incorrect; " + str(err))


def get_slack_users(slack_client):
    """
Getting a dictionary of real (not bots) and active (not deleted) Slack users with user name as a key and user id as a value

    :param slack_client: SlackClient which makes API Calls to the Slack Web API
    :type slack_client: instance of slackclient.client.SlackClient
    :return slack_users: real and active Slack users
    :rtype slack_users: dictionary
    """
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
    """
In case there is a match between user's DOB from google spreadsheet and the current date,
Slack sends a personal message to a Slack user.
In case the user doesn't exist in Slack, a warning is logged.
In case the user exists in Slack, Slack sends b-day notification to #general channel.

    :param slack_users: real and active Slack users
    :type slack_users: dictionary
    :param gsheet_users: contains user's full names and user's DOBs
    :type gsheet_users: list of dictionaries
    :param slack_client: SlackClient which makes API Calls to the Slack Web API
    :type slack_client: instance of slackclient.client.SlackClient
    """
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
    JSON_FILE = '/home/ycherkasova/PycharmProjects/MyProject-7540ad0415e5.json'
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
