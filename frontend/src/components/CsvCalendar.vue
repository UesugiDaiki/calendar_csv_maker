<template>
    <div class="csv-calendar mb-3">
        <full-calendar :options="calendarOptions" />
    </div>
    <to-flask :events="events" :calendarEvents="calendarOptions.events"/>

    <div class="d-flex justify-content-between mb-3">
        <!-- csvのダウンロード -->
        <button type="button" class="btn btn-primary" @click="downloadCsv">Donload csv</button>
        <!-- googleカレンダーに登録 -->
        <button type="button" class="btn btn-primary" @click="registGoogle">Register in Google calendar</button>
    </div>

    <!-- トースト -->
    <div class="toast align-items-center text-bg-primary border-0" role="alert" aria-live="assertive"
        aria-atomic="true">
        <div class="d-flex">
            <div class="toast-body">
                Hello, world! This is a toast message.
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"
                aria-label="Close"></button>
        </div>
    </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue3'
import interactionPlugin from '@fullcalendar/interaction'
import dayGridPlugin from '@fullcalendar/daygrid'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { getCsv, registGoogleCalendar } from '@/functions/ToFlask.js'

export default {
    components: {
        FullCalendar,
    },
    props: {
        events: Object,
        checkedEvents: Array,
    },
    data() {
        return {
            calendarOptions: {
                // カレンダーの設定
                // locale: 'ja',
                height: 550,
                plugins: [dayGridPlugin, interactionPlugin],
                initialView: 'dayGridMonth',
                selectable: true,
                headerToolbar: {
                    start: 'title',
                    center: '',
                    end: 'today prev,next'
                },
                // 予定
                events: [],
                // メソッド
                dateClick: this.dateClick,
                eventClick: this.eventClick,
                select: this.select,
            },
        }
    },
    computed: {
        // チェックされているが入力されていない予定があるか
        existNullEvent() {
            let exist = false
            for (let i = 0; i < Object.keys(this.checkedEvents).length; i++) {
                let checkedEvent = this.events.find(object => object.eventId === this.checkedEvents[i])
                Object.keys(checkedEvent).forEach(function (key) {
                    if (checkedEvent[key] === '') {
                        exist = true
                    }
                })
            }
            return exist
        }
    },
    methods: {
        // 日付を選択して予定追加
        select(arg) {
            if (this.existNullEvent) {
                // トーストを表示
                toast("未入力の予定があります", {
                    "autoClose": 2000,
                    "theme": "colored",
                    "type": "error",
                    "position": "bottom-center",
                    "hideProgressBar": true,
                    "transition": "slide",
                })
            } else {
                // 選択された日数を取得
                let selectDates = (arg.end - arg.start) / 86_400_000
                // チェックされている予定のみ追加
                for (let i = 0; i < this.checkedEvents.length; i++) {
                    // チェックされている予定を1つ格納
                    let checkedEvent = this.events.find(object => object.eventId === this.checkedEvents[i])
                    let eventId = checkedEvent.eventId
                    let color = checkedEvent.color
                    for (let j = 0; j < selectDates; j++) {
                        let dateStr = this.formatDate(arg.start, j)
                        if (!this.isExistEvent(eventId, dateStr)) {
                            this.createEvent(eventId, dateStr, color)
                        }
                    }
                }
            }
        },
        // 予定をクリックして削除
        // 参考:https://qiita.com/diescake/items/70d9b0cbd4e3d5cc6fce
        eventClick(arg) {
            this.calendarOptions.events = this.calendarOptions.events.filter(function (event) {
                return event.id !== Number(arg.event.id)
            })
        },
        // 予定作成
        createEvent(eventId, dateStr, color) {
            this.calendarOptions.events.push({
                id: this.createEventId(),
                eventId: eventId,
                start: dateStr,
                color: color,
            })
        },
        // 消された予定の削除
        removeCalendarEvent(eventId) {
            this.calendarOptions.events = this.calendarOptions.events.filter(function (event) {
                return event.eventId !== eventId
            })
        },
        // 新しい予定のidを取得
        createEventId() {
            let i = -1
            let isNewNum = false
            while (!isNewNum) {
                i++
                isNewNum = true
                for (let j = 0; j < this.calendarOptions.events.length; j++) {
                    if (i === this.calendarOptions.events[j].id) {
                        isNewNum = false
                    }
                }
            }
            return i
        },
        // 日付をYYYY-MM-DDの書式で返すメソッド
        // 参考:https://qiita.com/toshimin/items/5f13c3b4c28825219231
        formatDate(dt, afterDt) {
            var y = dt.getFullYear();
            var m = ('00' + (dt.getMonth() + 1)).slice(-2);
            var d = ('00' + (dt.getDate() + afterDt)).slice(-2);
            return (y + '-' + m + '-' + d);
        },
        // すでに存在する予定か判定
        isExistEvent(eventId, dateStr) {
            let isExist = false
            for (let i = 0; i < this.calendarOptions.events.length; i++) {
                if (this.calendarOptions.events[i].eventId === eventId && this.calendarOptions.events[i].start === dateStr) {
                    isExist = true
                }
            }
            return isExist
        },
        // CSVファイルダウンロード
        async downloadCsv() {
            let data = ''
            let csvData = await getCsv(this.events, this.calendarOptions.events)
            Object.keys(csvData).forEach(function (key) {
                data += csvData[key]
            })
            data = data.slice(0, -5)

            // csv形式に変換してダウンロード
            // 参考:https://samehack.com/javascript-csv-download/
            const bom = new Uint8Array([0xef, 0xbb, 0xbf]);
            const blob = new Blob([bom, data], { type: "text/csv" });
            const objectUrl = URL.createObjectURL(blob);
            const downloadLink = document.createElement("a");
            const fileName = "calendar.csv";
            downloadLink.download = fileName;
            downloadLink.href = objectUrl;
            downloadLink.click();
            downloadLink.remove();
        },
        // Googleカレンダーに登録
        async registGoogle() {
            let responseData = await registGoogleCalendar(this.events, this.calendarOptions.events)
            if (responseData.error) {
                // トーストを表示
                toast("登録に失敗しました", {
                    "autoClose": 2000,
                    "theme": "colored",
                    "type": "error",
                    "position": "bottom-center",
                    "hideProgressBar": true,
                    "transition": "slide",
                })
            } else {
                // トーストを表示
                toast("登録しました", {
                    "autoClose": 2000,
                    "theme": "colored",
                    "type": "success",
                    "position": "bottom-center",
                    "hideProgressBar": true,
                    "transition": "slide",
                })
            }
        }
    },
}
</script>