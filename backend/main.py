from flask import Flask, render_template, redirect, url_for, jsonify, request, make_response
from download_csv import make_csv_file, make_csv_data
from register_calendar import register_google_calendar

app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')
app.config['JSON_AS_ASCII'] = False # 文字化け防止

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def index(path):
    return render_template('index.html')

# csvファイルを作成してダウンロード
@app.route("/api/downloadCsv", methods=["POST"])
def get_csv():
    events = request.json["events"]
    calendarEvents = request.json["calendarEvents"]

    response = make_response()
    response.data = make_csv_file(events, calendarEvents)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = u'attachment; filename=calendar.csv'

    return response

# Googleカレンダーに登録
@app.route("/api/registGoogleCalendar", methods=["POST"])
def regist_calendar():
    events = request.json["events"]
    calendarEvents = request.json["calendarEvents"]

    register_google_calendar(make_csv_data(events, calendarEvents))

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)