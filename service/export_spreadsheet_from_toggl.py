import gspread
import requests
import external_setting as es
from datetime import timedelta
from requests.auth import HTTPBasicAuth
from service.util import get_now_str, convert_list_to_comma_str
from oauth2client.service_account import ServiceAccountCredentials


def get_credentials_to_gspread():
    # スプレッドシートへのアクセスURL
    scope = ["https://spreadsheets.google.com/feeds"]

    # スプレッドシートへのアクセス権を返す
    return ServiceAccountCredentials.from_json_keyfile_name(es.gcp_service_account_secret_key_file_path, scope)


def select_gspread_sheet(service_account_credentials, target_sheet):
    # スプレッドシート認証
    auth_gspread = gspread.authorize(service_account_credentials)

    # スプレッドシートのキー
    _gspread_key = es.gspread_key

    # 対象のスプレッドシートを開く
    # TODO open_by_urlならtarget_sheetを以下で指定しなくてもいい？
    target_gspread = auth_gspread.open_by_key(_gspread_key)

    # 対象のワークシートを指定
    return target_gspread.worksheet(target_sheet)


def get_toggl_workspace_id():
    # togglのAPIトークン
    _toggl_api_token = es.toggl_api_token

    if not _toggl_api_token:
        raise Exception("toggl_api_tokenが取得できません")

    response = requests.get("https://www.toggl.com/api/v8/workspaces", auth=(_toggl_api_token, "api_token"))

    user_toggle_data = response.json()[0]

    workspace_id = user_toggle_data.get("id")

    if not workspace_id:
        print("workspace_idが取得できませんでした")
        raise Exception("workspace_idが取得できませんでした")

    return workspace_id


def get_toggl_data(workspace_id, since_date):
    # togglのAPIトークン
    _toggl_api_token = es.toggl_api_token

    # データ取得開始日
    since_date = since_date

    # データ取得終了日
    until_date = get_now_str()

    # toggleAPIのURL
    toggl_api_url = "https://toggl.com/reports/api/v2/details"

    _params = {
        "user_agent": es.regist_mail_address_at_toggl,
        "workspace_id": workspace_id,
        "since": since_date,
        "until": until_date
    }

    try:
        # togglAPIからデータを取得
        response = requests.get(toggl_api_url, auth=HTTPBasicAuth(_toggl_api_token, 'api_token'), params=_params)

        return response

    except Exception as e:
        print("togglAPIからデータの取得に失敗しました")
        raise e


def export_toggl_data_to_gspread(toggl_data, worksheet):
    # togglから取得したデータをjson形式に変換
    toggl_data_json = toggl_data.json()["data"]

    if len(toggl_data_json) == 0:
        return

    try:
        # togglのデータをスプレッドシートに出力
        export_toggl_data = convert_toggl_data_for_gspread(toggl_data_json, worksheet)

    except Exception as e:
        print("スプレッドシートへの出力に失敗しています")
        raise e

    return export_toggl_data


def convert_toggl_data_for_gspread(toggl_data_json, worksheet):
    # 出力した文字列を返すための変数
    export_toggl_data = str()

    for toggl_data in toggl_data_json:
        append_data_list = list()

        # id
        toggl_id = str(toggl_data.get("id"))
        append_data_list.append(toggl_id)

        # 作業内容
        description = toggl_data.get("description")
        append_data_list.append(description)

        # プロジェクト
        project = toggl_data.get("project")
        append_data_list.append(project)

        # 作業時間
        dur = toggl_data.get("dur")
        td = timedelta(milliseconds=dur)
        td_str = str(td)
        append_data_list.append(td_str)

        # 開始時間
        toggl_start_date = toggl_data.get("start")
        start_date_str = str(toggl_start_date[0:10])
        append_data_list.append(start_date_str)

        # 終了時間
        toggl_end_date = toggl_data.get("end")
        end_date_str = str(toggl_end_date[0:10])
        append_data_list.append(end_date_str)

        # タグ
        tags_list = sorted(toggl_data.get("tags"))
        if tags_list:
            tags_str = convert_list_to_comma_str(tags_list)
            append_data_list.append(tags_str)

        # 最終行にデータを追加する
        worksheet.append_row(append_data_list)

        # 出力したデータを改行付きの文字列にする
        export_toggl_data += "{}\n".format(convert_list_to_comma_str(append_data_list))

    return export_toggl_data
