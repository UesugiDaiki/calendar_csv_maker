from io import StringIO
import csv

# データからcsvファイル作成
def make_csv_file(events, calendarEvents):
    file = StringIO()
    writer = csv.writer(file)
    writer.writerows(make_csv_data(events, calendarEvents))
    csv_data = file.getvalue()
    StringIO().close()

    return csv_data

# csvファイルの内容作成
def make_csv_data(events, calendarEvents):
    result = [make_csv_head()]

    for i in range(len(calendarEvents)):
        calendarEvent = calendarEvents[i]
        eventSummery = get_event_summery(events, calendarEvent["eventId"])

        subject = eventSummery["title"]
        startDate = calendarEvent["start"].replace('-', '/')
        startTime = eventSummery["startTime"]
        endTime = eventSummery["endTime"]

        result.append([subject, startDate, startTime, '', endTime, '', '', '', ''])

    return result

# 予定のIDの予定情報を取得する
def get_event_summery(events, eventId):
    for i in range(len(events)):
        if events[i]["eventId"] == eventId:
            result = events[i]

    return result

# googleカレンダー用csvファイルのヘッダー部分作成
def make_csv_head():
    return ["Subject","Start Date","Start Time","End Date","End Time","All Day Event","Description","Location","Private"]
