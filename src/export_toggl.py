import pandas as pd
from credentials import GSPREAD_KEY
from service.utils import get_now_str
from service.gsp import open_gspread
from service.log import (
    LogExport, 
    Logger
)
from service.decorator import (
    output_log, 
    notice_slack
)
from service.toggl import (
    convert_for_gspread, 
    get_toggl_data
)

logger = Logger()
log_export = LogExport("toggl.txt")
test_log_export = LogExport("test.txt")
target_sheet = "toggl"


# @notice_slack
@output_log
def main():

    try:
        since_date = input("データ取得開始日を入力してください (例)2021-04-01\n")

        # 入力がない場合は今日の日付をデータ取得開始日とする
        if not since_date:
            since_date = get_now_str()

        # スプレッドシートを開く
        gspread = open_gspread(GSPREAD_KEY)

        # スプレッドシートのワークシートを選択
        worksheet = gspread.worksheet(target_sheet)

        # togglのAPIに接続し、json形式でデータを取得
        toggl_data_json = get_toggl_data(since_date)

        if len(toggl_data_json) == 0:
            return

        export_toggl_data = [convert_for_gspread(toggl_data) for toggl_data in toggl_data_json]
        
        # togglのデータをスプレッドシートに出力
        worksheet.append_rows(export_toggl_data)

        log_export.output_log_list(export_toggl_data)
        log_export.output_log("正常にデータが出力されました")

        test_work_spreadsheet()

    except Exception as e:
        print(logger.exception('エラー内容'))
        log_export.output_error_log(e)


# TODO 名前適当
def test_work_spreadsheet():
    # スプレッドシートを開く
    gspread = open_gspread(GSPREAD_KEY)

    # スプレッドシートのワークシートを選択
    worksheet = gspread.worksheet(target_sheet)

    # スプレッドシートのデータを全て取得
    spreadsheet_data = worksheet.get_all_values()

    df = pd.DataFrame(spreadsheet_data[1:], columns=spreadsheet_data[0])

    test_log_export.output_log(df['id'])


if __name__ == "__main__":
    main()
