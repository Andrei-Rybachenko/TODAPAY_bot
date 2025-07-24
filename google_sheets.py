import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = "TODA_PAY_Users"
CRED_FILE = "credentials.json"  # Путь к JSON-файлу ключа от сервисного аккаунта

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CRED_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1  # Первый лист в таблице


def save_user_to_sheet(username, user_id, time):
    sheet.append_row([username, str(user_id), time])


def save_resume_to_sheet(username, user_id, email, summary, time):
    resume_sheet = client.open(SHEET_NAME).worksheet("Resumes")
    resume_sheet.append_row([username, str(user_id), email, summary, time])
