import requests
from datetime import timedelta
from requests.auth import HTTPBasicAuth
from service.utils import convert_list_to_comma_str
from service.utils import get_now_str
from credentials import (
  TOGGL_API_TOKEN,
  TOGGL_MAIL_ADDRESS
)

# togglAPIのURL
TOGGL_API_URL = "https://api.track.toggl.com/reports/api/v2/details"
TOGGL_WORKSPACES_URL = "https://api.track.toggl.com/api/v8/workspaces"


def get_workspace_id():

    response = requests.get(TOGGL_WORKSPACES_URL, auth=(TOGGL_API_TOKEN, "api_token"))

    if not (user_toggl_data := response.json()[0]):
        print("Togglからデータの取得ができませんでした")
        raise Exception("Togglからデータの取得ができませんでした")

    return user_toggl_data.get("id")


def get_toggl_data(since_date):

    _params = {
        "user_agent": TOGGL_MAIL_ADDRESS,
        "workspace_id": get_workspace_id(),
        "since": since_date,
        "until": get_now_str()
    }

    try:
        # togglAPIからデータを取得
        response = requests.get(TOGGL_API_URL, auth=HTTPBasicAuth(TOGGL_API_TOKEN, 'api_token'), params=_params)

        return response.json()["data"]

    except Exception as e:
        print("togglAPIからデータの取得に失敗しました")
        raise e

def convert_for_gspread(toggl_data):

    id = str(id) if (id := toggl_data.get("id")) else ""
    description = toggl_data.get("description", "")
    project = toggl_data.get("project", "")

    dur = toggl_data.get("dur", "")
    td_str = str(timedelta(milliseconds=dur))

    start = toggl_data.get("start")
    start_date_str = str(start[0:10])

    end = toggl_data.get("end")
    end_date_str = str(end[0:10])

    if tags_list := toggl_data.get("tags", []):
        tags_str = convert_list_to_comma_str(sorted(tags_list))

    return [id, description, project, td_str, start_date_str, end_date_str, tags_str]
