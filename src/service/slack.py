import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from service.log import LogExport


log_export = LogExport("toggl.txt")


def send2slack(webhook_url, channel_name, message):
    slack_message = {
        'channel': channel_name,
        'attachments': [
            {
                'fields': [
                    {
                        'value': message
                    }
                ]
            }
        ]
    }

    request = Request(webhook_url, json.dumps(slack_message).encode('utf-8'))

    try:
        response = urlopen(request)
        response.read()
        log_export.output_log('Slack message posted to {}'.format(channel_name))
        log_export.output_log('Slack message: {}'.format(message))

    except HTTPError as e:
        log_export.output_error_log(e)

    except URLError as e:
        log_export.output_error_log(e)

