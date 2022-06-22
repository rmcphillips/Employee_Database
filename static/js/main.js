// Dismiss the alert
if (document.getElementById("alert") !== null) {
    let alert = document.getElementById("alert");

    setTimeout(() => {
        alert.style.display = "none"
    }, 3000);
}

// Expands row on click in case they have text-truncate class 
const rows = document.getElementsByClassName("text-truncate")

for (let i = 0; i < rows.length; i++) {
    const element = rows[i];
    element.addEventListener("click", () => {
        if (element.classList.contains("text-truncate")) {
            element.classList.remove("text-truncate")
        }
        else {
            element.classList = "text-truncate"
        }
    })
}




