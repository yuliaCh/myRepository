# -*- encoding: utf-8 -*-
from datetime import date
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from slackclient import SlackClient, exceptions
import logging
import sys
#import json
import argparse
import yaml
import StringIO
import time
import smtplib
from email.MIMEText import MIMEText
from httplib2 import HttpLib2Error
from requests import RequestException
from socket import error


def create_parser():
    """
Creating ArgumentParser object with a command-line argument

    :return: parser: ArgumentParser object
    """
    parser = argparse.ArgumentParser(description='''SlackBot sends birthday congratulations
to employees via Slack messenger based on their date of birth provided in the google spreadsheet.
 In order for the script to run successfully, positional config argument should be supplied.''')
    parser.add_argument('config', type=argparse.FileType(), help='''config file,
     contains slack and google account credentials, and other customized data.''')

    return parser


def set_logging(log_file):
    """
Setting logging to a file and to a variable. Logs stored in the variable will then be emailed to HR specialist.
    :param log_file: a path to the file, where logs will be written to
    :type log_file: string
    :return log_string: logs which latter will be sent to the user
    :rtype log_string: StringIO object
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filename=log_file)
    logger.setLevel(logging.INFO)
    log_string = StringIO.StringIO()
    console_handler = logging.StreamHandler(log_string)
    console_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(fmt='%(asctime)s  %(levelname)s:  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return log_string


def open_gsheet(gsheet_credentials, gsheet_name):
    """
Getting access to sheet1 of google spreadsheet.
In case there is a connection or gspread api issue, http request is sent out for the second time in 5 seconds.
If an attempt is unsuccessful, the issue gets logged and the script exits.

    :param gsheet_credentials: google spreadsheet credentials from json file
    :type gsheet_credentials: ServiceAccountCredentials object
    :param gsheet_name: name of google spreadsheet containing employees' dates of birth
    :type gsheet_name: string
    :return activated_sheet: accessed sheet1 of google spreadsheet
    :rtype activated_sheet: Worksheet object
    """
    try:
        client = gspread.authorize(gsheet_credentials)
        activated_sheet = client.open(gsheet_name).sheet1
    except (gspread.exceptions.GSpreadException, HttpLib2Error):
        time.sleep(5)
        try:
            client = gspread.authorize(gsheet_credentials)
            activated_sheet = client.open(gsheet_name).sheet1
        except (gspread.exceptions.GSpreadException, HttpLib2Error) as err:
            logging.error("An error occurred while trying to access google spreadsheet. \
Error type: {type}. Error content: {content}".format(type=type(err),content=str(err)))
            sys.exit("Process finished with exit code 1")
    return activated_sheet


def get_gsheet_users(activated_sheet):
    """
Getting a list of dictionaries containing users' full name and date of birth from sheet1 of google spreadsheet.
In case there is a connection or gspread api issue, http request is sent out for the second time in 5 seconds.
If an attempt is unsuccessful, the issue gets logged and the script exits.

    :param activated_sheet: accessed sheet1 of google spreadsheet
    :type activated_sheet: Worksheet object
    :return gsheet_users: users' full name and date of birth from sheet1
    :rtype gsheet_users: list of dictionaries
    """

    try:
        gsheet_values = activated_sheet.get_all_values()
    except (gspread.exceptions.GSpreadException, RequestException):
        time.sleep(5)
        try:
            gsheet_values = activated_sheet.get_all_values()
        except (gspread.exceptions.GSpreadException, RequestException) as err:
            logging.error("An error occurred while trying to get google spreadsheet values. \
Error type: {type}. Error content: {content}".format(type=type(err),content=str(err)))
            sys.exit("Process finished with exit code 1")
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
            logger.warning("{name}: date of birth format is incorrect; {err}".format(name = user["name"], err = str(err)))


def get_slack_users(slack_client):
    """
Getting a dictionary of real (not bots) and active (not deleted) Slack users with user name as a key and user id as a value.
In case there is a connection or Slack api issue, http request is sent out for the second time in 5 seconds.
If an attempt is unsuccessful, the issue gets logged and the script exits.

    :param slack_client: SlackClient which makes API Calls to the Slack Web API
    :type slack_client: SlackClient object
    :return slack_users: real and active Slack users
    :rtype slack_users: dictionary
    """
    slack_users = {}
    try:
        user_profiles = slack_client.api_call("users.list")["members"]
    except (exceptions.SlackClientError, RequestException):
        time.sleep(5)
        try:
            user_profiles = slack_client.api_call("users.list")["members"]
        except (exceptions.SlackClientError, RequestException) as err:
            logging.error(
                "An error occurred while trying to get slack user list. \
Error type: {type}. Error content: {content}".format(type=type(err),content=str(err)))
            sys.exit("Process finished with exit code 1")
    #logging.debug("user_profile:\n {}".format(json.dumps(user_profiles, indent = 2)))
    for user in user_profiles:
        if user["id"] != "USLACKBOT" and not user["deleted"] and not user["is_bot"]:
            name = user["real_name"].strip().lower()
            id = user["id"]
            slack_users[name] = id
    #logging.debug("slack_users:\n {}".format(slack_users))
    return slack_users


def post_slack_message(slack_users, gsheet_users, slack_client, hr_name, hr_alias):
    """
This is a main function which initiates sending messages to Slack users and then calls other functions.
In case there is a match between user's date of birth from google spreadsheet and the current date,
"try_sending_slack_message" function is initiated. After that, "send_confirmation_to_hr" function is initiated.

    :param slack_users: real and active Slack users
    :type slack_users: dictionary
    :param gsheet_users: users' full name and date of birth from sheet1 of google spreadsheet
    :type gsheet_users: list of dictionaries
    :param slack_client: SlackClient which makes API Calls to the Slack Web API
    :type slack_client: SlackClient object
    :param hr_name: HR specialist's name
    :type hr_name: string
    :param hr_alias: HR specialist's alias used in Slack
    :type hr_alias: string
    """
    current_date = date.today().strftime("%-d-%b")
    notifications_sent = []

    for user in gsheet_users:
        if user["date"] == current_date and user["name"].lower() != hr_name:
            try_sending_slack_message(slack_client, slack_users, user, notifications_sent, hr_alias)
        elif user["date"] == current_date and user["name"].lower() == hr_name:
            try_sending_slack_message(slack_client, slack_users, user, notifications_sent)
    send_confirmation_to_hr(slack_client, notifications_sent, slack_users, hr_name)


def try_sending_slack_message(slack_client, slack_users, user, notifications_sent, hr_alias=None):
    """
This function initiates "send_slack_message" function, which sends a personal message to a Slack user.
In case the user doesn't exist in Slack, a warning is logged.
In case there is a connection or Slack api issue, http request is sent out for the second time in 5 seconds.
If an attempt is unsuccessful, the issue gets logged as a warning.
In case "send_slack_message" finishes successfully, the user name, to whom congratulation has been sent, gets added
to notifications_sent list.

    :param slack_client: SlackClient which makes API Calls to the Slack Web API
    :type slack_client: SlackClient object
    :param slack_users: real and active Slack users
    :type slack_users: dictionary
    :param user: dictionary consisting of a user name and its corresponding slack id
    :type user: dictionary
    :param notifications_sent: a list of employees to whom birthday congratulations have been sent
    :type notifications_sent: list
    :param hr_alias: HR specialist's Slack alias
    :type hr_alias: string
    """
    try:
        send_slack_message(slack_client, slack_users, user, hr_alias)
    except KeyError:
        logger.warning("{} does not exist in Slack".format(user["name"]))
    except (exceptions.SlackClientError, RequestException):
        time.sleep(5)
        try:
            send_slack_message(slack_client, slack_users, user, hr_alias)
        except (exceptions.SlackClientError, RequestException) as err:
            logger.warning(
                "An error occurred while trying to send slack message. \
Error type: {type}. Error content: {content}".format(type=type(err), content=str(err)))
        else:
            notifications_sent.append(user["name"].encode('ascii', 'ignore'))
            logger.info("Birthday congratulation has been sent to {} via Slack".format(user["name"]))
    else:
        notifications_sent.append(user["name"].encode('ascii', 'ignore'))
        logger.info("Birthday congrtulation has been sent to {} via Slack".format(user["name"]))



def send_slack_message(slack_client, slack_users, user, hr_alias=None):
    """
This function sends a personal message to a Slack user.
In case there is a connection or Slack api issue, http request is sent out for the second time in 5 seconds.
If an attempt is unsuccessful, the issue gets logged as a warning.

    :param slack_client: SlackClient instance
    :type slack_client: SlackClient instance
    :param slack_users: real and active Slack users
    :type slack_users: dictionary
    :param user: dictionary consisting of a user name and its corresponding slack id
    :type user: dictionary
    :param hr_alias: HR specialist's Slack alias
    :type hr_alias: string
    """
    if hr_alias is not None:
        slack_client.api_call("chat.postMessage",
                              channel=slack_users[user["name"].lower()],
                              text=text_1.format(hr_alias),
                              as_user="true")
    else:
        slack_client.api_call("chat.postMessage",
                              channel=slack_users[user["name"].lower()],
                              text=text_2,
                              as_user="true")


def send_confirmation_to_hr(slack_client,notifications_sent, slack_users, hr_name):
    """
This function sends a list of users, to whom congratulations have been delivered, to HR person.
In case there is a connection or Slack api issue, http request is sent out for the second time in 5 seconds.
If an attempt is unsuccessful, the issue gets logged and the script exits.

    :param slack_client: SlackClient instance
    :type slack_client: SlackClient instance
    :param notifications_sent: a list of employees to whom birthday congratulations have been sent
    :type notifications_sent: list
    :param slack_users: real and active Slack users
    :type slack_users: dictionary
    :param hr_name: HR specialist's name
    :type hr_name: string
    """
    if notifications_sent != []:
        try:
            slack_client.api_call("chat.postMessage", channel=slack_users[hr_name],
                                  text="{date}: Birthday notification has been sent to {name}".
                                  format(date=date.today().strftime("%d-%b"),
                                         name=str(notifications_sent).strip("[]").replace("'", "")),
                                  as_user="true")
        except (exceptions.SlackClientError, RequestException):
            time.sleep(5)
            try:
                slack_client.api_call("chat.postMessage", channel=slack_users[hr_name],
                                      text="{date}: Birthday notification has been sent to {name}".
                                      format(date=date.today().strftime("%d-%b"),
                                             name=str(notifications_sent).strip("[]").replace("'", "")),
                                      as_user="true")
            except (exceptions.SlackClientError, RequestException) as err:
                logger.warning("An error occurred while trying to send slack message. \
Error type: {type}. Error content: {content}".format(type=type(err), content=str(err)))
            else:
                logging.info("List of sent notifications has been provided to {} via Slack".format(hr_name))
        else:
            logging.info("List of sent notifications has been provided to {} via Slack".format(hr_name))


def end_string_logging(log_string):
    """
Storing log content into a variable and closing the log string.

    :param log_string: logs which latter will be sent to the HR specialist
    :type log_string: StringIO object
    :return log_content: logs stored in a variable to be sent out to HR specialist's gmail box afterwards
    :rtype log_content: string
    """
    log_content = log_string.getvalue()
    log_string.close()
    #logging.debug(log_content)
    return log_content


def send_mail(sender, password, recipient, log_content, subject):
    """
The main function which initiates creating and sending email with logs to HR specialist.
In case there is SMTP issue, http request is sent out for the second time in 5 seconds.
If an attempt is unsuccessful, the issue gets logged as a warning.

    :param sender: gmail address from which emails with logs will be sent out
    :type sender: string
    :param password: gmail password related to gmail address from which emails with logs will be sent out
    :type password: string
    :param recipient: gmail address of HR specialist
    :type recipient: string
    :param log_content: logs stored in a variable to be sent out to HR specialist's gmail box afterwards
    :type log_content: string
    :param subject: email subject
    :type subject: string
    """
    if log_content is not None:
        message = create_message(sender, recipient, subject, log_content)
        try:
            try_sending_mail(sender, recipient, password, message)
        except (smtplib.SMTPException, error):
            time.sleep(5)
            try:
                try_sending_mail(sender, recipient, password, message)
            except (smtplib.SMTPException, error) as err:
                logging.warning("An error occurred while trying to send an email to {addressee}. \
Error type: {type}. Error content: {content}".format(addressee = (recipient), type=type(err), content=str(err)))
            else:
                logging.info("Email with logs has been sent to {}".format(recipient))
        else:
            logging.info("Email with logs has been sent to {}".format(recipient))


def create_message(sender, recipient, subject, log_content):
    """
Creating a message to be sent out.

    :param sender: gmail address from which emails with logs will be sent out
    :type sender: string
    :param recipient: gmail address of HR specialist
    :type recipient: string
    :param subject: email subject
    :type subject: string
    :param log_content: logs stored in a variable to be sent out to HR specialist's gmail box afterwards
    :type log_content: string
    :return message: Message which will be sent out
    :rtype: MIME Message object
    """
    message = MIMEText(log_content)
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    return message


def try_sending_mail(sender, recipient, password, message):
    """
Sending email with logs to HR specialist.

    :param sender: gmail address from which emails with logs will be sent out
    :type sender: string
    :param recipient: gmail address of HR specialist
    :type recipient: string
    :param password: gmail password related to gmail address from which emails with logs will be sent out
    :type password: string
    :param message: Message which will be sent out
    :type message: MIME Message object
    """
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(sender, password)
    server.sendmail(sender, recipient, message.as_string())
    server.close()

def main():

    parser = create_parser()
    config = yaml.load(parser.parse_args().config)
    log_string = set_logging(config["log_file"])
    slack_client = SlackClient(config["slack_token"])
    gsheet_credentials = ServiceAccountCredentials.from_json_keyfile_name(config["json_file"], config["scope"])
    activated_sheet = open_gsheet(gsheet_credentials,config["gsheet_name"])
    gsheet_users = get_gsheet_users(activated_sheet)
    validate_gsheet_date(gsheet_users)
    slack_users = get_slack_users(slack_client)
    post_slack_message(slack_users, gsheet_users, slack_client,config["hr_name"].strip().lower(), config["hr_alias"])
    log_content = end_string_logging(log_string)
    send_mail(config["sender_address"], config["password"], config["recipient_address"], log_content, config["subject"])


if __name__ == '__main__':

    text_1 = \
"""Привет, поздравляем тебя с Днем Рождения! :tada: :birthday:
Пускай сегодня работа сама себя сделает, а день будет легким и полным приятных сюрпризов. \
Желаем ясного неба над головой, оптимизма и счастья в душе! Радости тебе, удачи и прекрасного настроения!
По такому приятному случаю мы приготовили тебе небольшой подарок :gift: \
Напиши {}, чтобы узнать подробности!"""

    text_2 = \
"""Привет, поздравляем тебя с Днем Рождения! :tada: :birthday:
Пускай сегодня работа сама себя сделает, а день будет легким и полным приятных сюрпризов. \
Желаем ясного неба над головой, оптимизма и счастья в душе! Радости тебе, удачи и прекрасного настроения!"""

    logger = logging.getLogger(__name__)

    main()
