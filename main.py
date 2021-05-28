import pandas as pd
from service.log import Logger
from service.decorator import output_log
from service.decorator import notice_slack
from service.util import get_now_str
from service.import_spreadsheet import get_data_from_spreadsheet
from service.export_spreadsheet_from_toggl import get_toggl_data
from service.export_spreadsheet_from_toggl import get_toggl_workspace_id
from service.export_spreadsheet_from_toggl import get_credentials_to_gspread
from service.export_spreadsheet_from_toggl import select_gspread_sheet
from service.export_spreadsheet_from_toggl import export_toggl_data_to_gspread

import external_setting as es

# Loggerにログファイルをセットする
logger = Logger("toggl.txt")
test_logger = Logger("test.txt")

target_sheet = "toggl"


# @notice_slack
# @output_log
def main():
    # export_gspread_from_toggl()

    test_work_spreadsheet()


def export_gspread_from_toggl():

    try:
        since_date = input("データ取得開始日を入力してください (例)2021-04-01\n")

        # 入力がない場合は今日の日付をデータ取得開始日とする
        if not since_date:
            since_date = get_now_str()

        # スプレッドシートへのアクセス権を取得
        service_account_credentials = get_credentials_to_gspread()

        # スプレッドシートのワークシートを選択
        worksheet = select_gspread_sheet(service_account_credentials, target_sheet)

        # togglのworkspaceIdを取得
        toggl_workspace_id = get_toggl_workspace_id()

        # togglのAPIに接続し、データを取得
        toggl_data = get_toggl_data(toggl_workspace_id, since_date)

        # togglのデータをスプレッドシートに出力
        export_toggl_data = export_toggl_data_to_gspread(toggl_data, worksheet)
        logger.output_log(export_toggl_data)

        logger.output_log("正常にデータが出力されました")

    except Exception as e:
        logger.output_error_log(e)


# TODO 名前適当
def test_work_spreadsheet():
    # スプレッドシートへのアクセス権を取得
    service_account_credentials = get_credentials_to_gspread()

    # スプレッドシートのワークシートを選択
    worksheet = select_gspread_sheet(service_account_credentials, target_sheet)

    # スプレッドシートのデータを全て取得
    spreadsheet_data = get_data_from_spreadsheet(worksheet)

    df = pd.DataFrame(spreadsheet_data[1:], columns=spreadsheet_data[0])

    test_logger.output_log(df['id'])


if __name__ == "__main__":
    main()
