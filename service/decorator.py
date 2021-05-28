import external_setting as es
from service.slack import send2slack
from service.log import Logger

# Loggerにログファイルをセットする
logger = Logger("toggl.txt")


def output_log(func):
    def wrapper(*args, **kwargs):
        logger.output_log("------------toggl出力処理 開始------------")
        response = func(*args, **kwargs)
        logger.output_log("------------toggl出力処理 終了------------")
        return response
    return wrapper


def notice_slack(func):
    def wrapper(*args, **kwargs):
        send2slack(es.review_day_url, 'review-day', '処理開始')
        response = func(*args, **kwargs)
        send2slack(es.review_day_url, 'review-day', '処理終了')
        return response
    return wrapper
