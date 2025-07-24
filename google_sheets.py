import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials


GOOGLE_CREDENTIALS = json.loads(os.getenv("GOOGLE_CREDENTIALS"))


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]


credentials = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS, scope)
client = gspread.authorize(credentials)

SHEET_NAME = "TODA_PAY_Users"


def save_resume_to_sheet(username, user_id, email, summary, timestamp):
    sheet = client.open(SHEET_NAME).worksheet("Resumes")
    sheet.append_row([username, str(user_id), email, summary, timestamp])


def save_user_to_sheet(username, user_id, timestamp):
    sheet = client.open(SHEET_NAME).sheet1
    sheet.append_row([username, str(user_id), timestamp])


def export_all_content():
    sheet = client.open(SHEET_NAME).worksheet("Resumes")
    return sheet.get_all_values()
