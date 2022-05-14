// set date and time to (date|time)-input fields

const makeDate = (date) => {
    // return date in ISO-8601 format
    const day = date.getDate().toString().padStart(2, "0"),
        month = date.getMonth().toString().padStart(2, "0"),
        year = date.getFullYear().toString()

    return `${year}-${month}-${day}`
}


const makeTime = (date) => {
    // return time in ISO-8601 format
    const hour = date.getHours().toString().padStart(2, "0"),
        minute = date.getMinutes().toString().padStart(2, "0"),
        second = date.getSeconds().toString().padStart(2, "0")

    return `${hour}:${minute}:${second}`
}


const addToDate = (date, y, m, d) => {
    // update given time with passed parameters and 
    // return new time
    const newDate = new Date()
    newDate.setFullYear(date.getFullYear() + y)
    newDate.setMonth(date.getMonth() + m)
    newDate.setDate(date.getDate() + d)

    return newDate
}
