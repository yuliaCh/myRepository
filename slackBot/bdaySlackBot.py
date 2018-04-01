from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from slackclient import SlackClient


def get_slack_user_names(user_profiles):
    slack_user_dict = {}

    for user in user_profiles:
        if not user["deleted"]:
            name = str(user["real_name"])
            id = str(user["id"])
            slack_user_dict[name] = id

    return slack_user_dict

def open_gsheet(creds):
    client = gspread.authorize(creds)
    sheet = client.open("Birthdays_test").sheet1
    gsheet_data = sheet.get_all_records()
    return gsheet_data

#Google spreadsheet needs to have a header for the column with full user names
def get_gspread_name_list(gs_data, date):
    gsheet_user_list = []
    for user in gs_data:
        if user['Date'] == date:
            gsheet_user_list.append(user['full name ENG'])
    return gsheet_user_list

def post_message(sl_dict, gs_list, sc):
    for user in sl_dict:
        for member in gs_list:
            if user == member:
                sc.api_call("chat.postMessage",
                            channel=sl_dict[user],
                            text="new message! - 4")
                sc.api_call("chat.postMessage",
                            channel="#general",
                            text="post to #general! - 4")


def main():
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    slack_user_profiles = slack_client.api_call("users.list")["members"]

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    JSON_FILE = '/home/yulia/python_projects/MyProject-d27a72192381.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)

    current_date = date.today().strftime("%d-%b")

    slack_user_dict = get_slack_user_names(slack_user_profiles)
    print(slack_user_dict)
    gsheet_data = open_gsheet(credentials)
    print(gsheet_data)
    gsheet_user_list = get_gspread_name_list(gsheet_data, current_date)
    print("gsheet_user_list")
    print(gsheet_user_list)
    post_message(slack_user_dict, gsheet_user_list, slack_client)
    print(post_message)



if __name__ == '__main__':
    main()
