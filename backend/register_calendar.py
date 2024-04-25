from flask import redirect
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def register_google_calendar(eventsData):
    # # カレンダーAPIのスコープを設定
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # ユーザー認証を行いAPIクライアントを作成
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('calendar', 'v3', credentials=creds)

    # イベントデータを作成して追加
    for i in range(len(eventsData)):
        if i != 0:
            # 時間を YYYY-MM-DDThh:mm:ss-00:00 に整形
            startDate = eventsData[i][1].replace('/', '-') + 'T' + eventsData[i][2] + ':00+09:00'
            endDate = eventsData[i][1].replace('/', '-') + 'T' + eventsData[i][4] + ':00+09:00'

            event = {
                'summary': eventsData[i][0],
                'start': {
                    'dateTime': startDate,
                },
                'end': {
                    'dateTime': endDate,
                },
            }

            # イベントを追加
            service.events().insert(calendarId='primary', body=event).execute()

# 参考:https://dev.classmethod.jp/articles/google-calendar-api-create-schedule/