from credentials import SLACK_URL
from service.slack import send2slack
from service.log import LogExport

# LogExportにログファイルをセットする
log_export = LogExport("toggl.txt")


def output_log(func):
    def wrapper(*args, **kwargs):
        log_export.output_log("------------toggl出力処理 開始------------")
        response = func(*args, **kwargs)
        log_export.output_log("------------toggl出力処理 終了------------")
        return response
    return wrapper


def notice_slack(func):
    def wrapper(*args, **kwargs):
        send2slack(SLACK_URL, 'review-day', '処理開始')
        response = func(*args, **kwargs)
        send2slack(SLACK_URL, 'review-day', '処理終了')
        return response
    return wrapper
