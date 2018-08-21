# -*- encoding: utf-8 -*-
from datetime import date
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from slackclient import SlackClient
import logging
import sys
import json
import argparse
import yaml


def create_parser():
    """
Creating ArgumentParser object, which contains provided command-line arguments

    :return: parser: ArgumentParser object
    """
    parser = argparse.ArgumentParser(description='''SlackBot sends birthday congratulations
to employees in Slack messenger based on provided google spreadsheet containing employees' dates of birth.
 In order for the program to run successfully, both arguments (slack token and json file with google account credentials)
 should be supplied. The arguments are not positional, but they are required.''')
    parser.add_argument('-c', '--config', required=True, type = argparse.FileType(), help='''yaml config file,
     containing slack token and path to json file with google account credentials; this argument is not positional,
      but it is required.''')

    return parser





def open_gsheet(gsheet_credentials):
    """
Getting access to sheet1 of google spreadsheet

    :param gsheet_credentials: google spreadsheet credentials from json file
    :type gsheet_credentials: ServiceAccountCredentials object
    :return activated_sheet: accessed sheet1 of google spreadsheet
    :rtype activated_sheet: Worksheet object
    """
    client = gspread.authorize(gsheet_credentials)
    activated_sheet = client.open("Bdays_autocongrats").sheet1
    return activated_sheet


def get_gsheet_users(activated_sheet):
    """
Getting a list of dictionaries containing users' full name and date of birth from sheet1 of google spreadsheet

    :param activated_sheet: accessed sheet1 of google spreadsheet
    :type activated_sheet: Worksheet object
    :return gsheet_users: users' full name and date of birth from sheet1
    :rtype gsheet_users: list of dictionaries
    """

    gsheet_values = activated_sheet.get_all_values()
    gsheet_users = []
    for value in gsheet_values:
        if value[0] != "" and value[0] != " ":
            sub_gsheet_users = {}
            name = value[0].strip()
            date = value[1]
            sub_gsheet_users["name"] = name
            sub_gsheet_users["date"] = date
            gsheet_users.append(sub_gsheet_users)
    #logging.debug(gsheet_users)
    return gsheet_users


def validate_gsheet_date(gsheet_users):
    """
Checking if user's date of birth is of a correct format. In case it is not, a warning is logged.

    :param gsheet_users: contains users' full name and date of birth
    :type gsheet_users: list of dictionaries
    """
    for user in gsheet_users:
        try:
            datetime.strptime(user["date"], "%d-%b")
        except ValueError as err:
            logging.warning("{name}: date of birth format is incorrect; {err}".format(name = user["name"], err = str(err)))


def get_slack_users(slack_client):
    """
Getting a dictionary of real (not bots) and active (not deleted) Slack users with user name as a key and user id as a value

    :param slack_client: SlackClient which makes API Calls to the Slack Web API
    :type slack_client: SlackClient object
    :return slack_users: real and active Slack users
    :rtype slack_users: dictionary
    """
    user_profiles = slack_client.api_call("users.list")["members"]
    #logging.debug("user_profile:\n {}".format(json.dumps(user_profiles, indent = 2)))
    slack_users = {}
    for user in user_profiles:
        if user["id"] != "USLACKBOT" and not user["deleted"] and not user["is_bot"]:
            name = user["real_name"].strip().lower()
            id = user["id"]
            slack_users[name] = id
    #logging.debug("slack_users:\n {}".format(slack_users))
    return slack_users


def post_slack_message(slack_users, gsheet_users, slack_client):
    """
In case there is a match between user's date of birth from google spreadsheet and the current date,
Slack sends a personal message to a Slack user.
In case the user doesn't exist in Slack, a warning is logged.

    :param slack_users: real and active Slack users
    :type slack_users: dictionary
    :param gsheet_users: users' full name and date of birth from sheet1 of google spreadsheet
    :type gsheet_users: list of dictionaries
    :param slack_client: SlackClient which makes API Calls to the Slack Web API
    :type slack_client: SlackClient object
    """
    current_date = date.today().strftime("%-d-%b")
    for user in gsheet_users:
        if user["date"] == current_date:
            try:
                slack_client.api_call("chat.postMessage",
                                      channel=slack_users[user["name"].lower()],
                                      text="""Привет, поздравляем тебя с Днем Рождения! :tada: :birthday:
Пускай сегодня работа сама себя сделает, а день будет легким и полным приятных сюрпризов. \
Желаем ясного неба над головой, оптимизма и счастья в душе! Радости тебе, удачи и прекрасного настроения!
По такому приятному случаю мы приготовили тебе небольшой подарок :gift: \
Напиши @obogdanova, чтобы узнать подробности!""",
                                      as_user="true")
                logging.info("Birthday notification has been sent to {}".format(user["name"]))
            except KeyError:
                logging.warning("{} does not exist in Slack".format(user["name"]))


def main():
    parser = create_parser()
    config_data = yaml.load(parser.parse_args().config)
    #logging.debug("config_data:\n {}".format(config_data))

    slack_token = config_data["slack_token"]
    json_file = config_data["json_file"]
    slack_client = SlackClient(slack_token)
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    gsheet_credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)

    activated_sheet = open_gsheet(gsheet_credentials)
    gsheet_users = get_gsheet_users(activated_sheet)
    validate_gsheet_date(gsheet_users)
    slack_users = get_slack_users(slack_client)
    post_slack_message(slack_users, gsheet_users, slack_client)


if __name__ == '__main__':
    print(date.today())
    print(date.today().strftime("%-d-%b"))
    file_location = '/home/yulia/study_repo/myRepository/slackBot/BdayBot/{dated_folder}/BdayBot_{dated_file}.txt'.format(dated_folder=date.today().strftime("%m-%Y"), dated_file=date.today())
    #file_location = '20180820.txt'
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=file_location,
                        filemode="w")
    main()
