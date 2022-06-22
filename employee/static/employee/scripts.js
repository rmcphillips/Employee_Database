window.scrollTo(0, document.body.scrollHeight);

const rowAttendance = document.getElementsByClassName("container bg-light p-3 mb-2")
const arr = Array.from(rowAttendance);
arr.splice(-5)


// SHOWS ONLY LAST 5 DAYS OF ATTENDANCE
for (let index = 0; index < arr.length; index++) {
    arr[index].style = "display: None;"
}
