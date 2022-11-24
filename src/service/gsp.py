import gspread
from credentials import (
  GCP_SECRET_KEY_FILE_PATH,
  GSPREAD_KEY
)
from oauth2client.service_account import ServiceAccountCredentials


# スプレッドシートを開く
def open_gspread(gspread_key):
    # スプレッドシートへのアクセスURL
    scope = ["https://spreadsheets.google.com/feeds"]

    # スプレッドシートへのアクセス権
    gspread_credentials = ServiceAccountCredentials.from_json_keyfile_name(GCP_SECRET_KEY_FILE_PATH, scope)

    # スプレッドシート認証
    auth_gspread = gspread.authorize(gspread_credentials)

    return auth_gspread.open_by_key(gspread_key)
