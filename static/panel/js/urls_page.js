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


const now = new Date()
const defaultExpireDateTime = new Date(addToDate(now, 0, 0, 10))


$("#start_date").val(makeDate(now))
$("#start_time").val(makeTime(now))

$("#expire_date").val(makeDate(defaultExpireDateTime))
$("#expire_time").val(makeTime(now))


// the "create-url-api" url
const protocol = $(location).attr("protocol")
const host = $(location).attr("host")
const url = `${protocol}//${host}/api/url/add/`

// Getting csrftoken to use in AJAX requests
const csrftoken = $("input[name=csrfmiddlewaretoken]").val()

// handle submit button
$("input[type=submit]").click((e) => {
    e.preventDefault()

    let payload = {}

    $("form[id=url_create_form]").serializeArray().forEach((val, key) => {
        payload[val.name] = val.value
    })

    // =============== A payload smaple ===============
    // payload = {
    //     url: "407",
    //     target: "https://archive.org",
    //     access_start: "2022-04-17 18:12:56",
    //     access_duration: "100 12:07:45",
    //     monitored: true,
    //     access_code: "helloworld",
    //     csrfmiddlewaretoken: csrftoken
    // }

    // send data to api
    $.ajax({
        url: url,
        type: "post",
        dataType: "json",
        data: JSON.stringify(payload),
        headers: { "X-CSRFToken": csrftoken },
        contentType: "application/json",
        success: (result, status, xhr) => { console.log(result, status, xhr) },
        error: (xhr, status, error) => { console.log(error, status, xhr) }

    })

    // 3 - update the error part if need and if not, check it true

    // 4 - after all of these, send the create request to host and update the page information
})