<template>
    <!-- 予定 -->
    <div class="mb-4">
        <div v-for="(event, index) in events" :key="event.eventId" class="d-flex justify-content-center mb-2">
            <!-- チェックボックス -->
            <input class="form-check-input my-auto" type="checkbox" :value="event.eventId" v-model="checkedEvents" checked>
            <!-- カラーピッカー -->
            <div class="px-2"><input type="color" class="form-control form-control-color" id="exampleColorInput"
                    v-model="event.color" title="Choose your color"></div>
            <!-- 予定名 -->
            <div class="px-2"><input class="form-control" type="text" placeholder="Event title"
                    v-model="event.title" aria-label="default input example"></div>
            <!-- 開始時間 -->
            <div class="px-2"><input class="form-control" type="time" name="example" v-model="event.startTime"></div>
            <p class="my-auto">-</p>
            <!-- 終了時間 -->
            <div class="px-2"><input class="form-control" type="time" name="example" v-model="event.endTime"></div>
            <!-- 予定削除ボタン -->
            <div class="px-2">
                <button type="button" class="btn btn-light" @click="removeEvent(index, event.eventId)">
                    <i class="bi bi-trash-fill"></i>
                </button>
            </div>
        </div>
        <!-- 予定追加ボタン -->
        <div class="my-1">
            <button type="button" class="btn btn-light" @click="addEvent">
                <i class="bi bi-plus"></i>
            </button>
        </div>
    </div>
    
    <!-- カレンダー -->
    <csv-calendar ref="calendar" :events="events" :checkedEvents="checkedEvents"/>
</template>

<script>
import CsvCalendar from '@/components/CsvCalendar.vue'
import 'bootstrap-icons/font/bootstrap-icons.css'

export default {
    components: {
        CsvCalendar
    },
    data() {
        return {
            events: [
                {
                    eventId: 0,
                    title: '',
                    startTime: '',
                    endTime: '',
                    color: '#57bca8',
                },
            ],
            checkedEvents: [0],
        }
    },
    methods: {
        // 予定の入力欄追加
        addEvent() { 
            let eventId = this.createEventId()
            this.events.push({
                eventId: eventId,
                title: '',
                startTime: '',
                endTime: '',
                color: this.createRandomColor(),
            })
            this.checkedEvents.push(eventId)
        },
        // 予定の入力欄とその予定を削除
        removeEvent(index, id) {
            // 子コンポーネントから予定を削除する
            this.$refs.calendar.removeCalendarEvent(id)
            // 入力欄を削除する
            this.events = this.events.filter(function(event) {
                return event.eventId !== id
            })
            this.checkedEvents = this.checkedEvents.filter(function(checked) {
                return checked !== id
            })
        },
        // 新しい予定のidを作成
        createEventId() {
            let i = -1
            let isNewNum = false
            while (!isNewNum) {
                i++
                isNewNum = true
                for (let j = 0; j < this.events.length; j++) {
                    if (i === this.events[j].eventId) {
                        isNewNum = false
                    }
                }
            }
            return i
        },
        // ランダムでまだ存在しない16進数カラーコードを生成
        // 参考:https://q-az.net/random-color-code/
        createRandomColor() {
            let isExist = true
            let randomColor = ''
            while (isExist) {
                isExist = false
                randomColor = '#'
                for (let i = 0; i < 6; i++) {
                    randomColor += "0123456789abcdef"[16 * Math.random() | 0]
                }
                
                for (let i = 0; i < this.events.length; i++) {
                    if (this.events[i].color === randomColor) {
                        isExist = true
                    }
                }
            }
            return randomColor
        }
    }
}
</script>