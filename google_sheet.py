from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'path/to/your-service-account-file.json'  # 替换为你的服务账户文件路径
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'  # 替换为你的Google Sheet ID

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

def append_row(values):
    sheet = service.spreadsheets()
    body = {'values': [values]}
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    return result
