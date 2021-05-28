from datetime import datetime


def get_now_datetime():
    return datetime.now()


# 日付型を文字列型に変換
def get_datetime_str(date):
    return date.strftime("%Y-%m-%d")


def get_now_str():
    # 今日の日付を取得
    now_date = get_now_datetime()

    # 今日の日付を%Y-%m-%d形式で文字列化
    return get_datetime_str(now_date)


# リスト型をカンマ区切りの文字列に変換
def convert_list_to_comma_str(list_data):
    return ",".join(list_data)


# リスト型を改行付きの文字列に変換
def convert_list_to_new_line_str(list_data):
    return "\n".join(list_data)
