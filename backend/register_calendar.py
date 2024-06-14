from __future__ import print_function
from flask import redirect
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

import pytz  # pytzモジュールをインポート
import os

def register_google_calendar(eventsData):
    # カレンダーAPIのスコープを設定
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None
    # token.jsonファイルにはユーザーのアクセスおよびリフレッシュトークンが保存されます。
    if os.path.exists('token.json'):
        # 既存の認証情報をロード
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 有効な認証情報がない場合、ユーザーにログインさせます。
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 認証情報が期限切れの場合、トークンをリフレッシュ
            creds.refresh(Request())
        else:
            # 新しい認証フローを開始
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # 次回の実行のために認証情報を保存します。
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

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