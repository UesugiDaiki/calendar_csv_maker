import axios from "axios"

// 予定情報をcsv形式で受け取る
export const getCsv = async function(events, calendarEvents) {
    try {
        const response = await axios.post("/api/downloadCsv", {events: events, calendarEvents: calendarEvents})
        return {...response.data, error: false}
    } catch(e) {
        console.log(e)
        return {error: true}
    }
}

// 予定情報をgoogleカレンダーに登録する
export const registGoogleCalendar = async function(events, calendarEvents) {
    try {
        const response = axios.post("/api/registGoogleCalendar", {events: events, calendarEvents: calendarEvents})
        return {...response.data, error: false}
    } catch (e) {
        console.log(e)
        return {error: true}
    }
}