const button = document.getElementById("message_btn")
const messageButton = document.getElementById("message_board")

document.addEventListener("DOMContentLoaded", () => {
    const timer = setTimeout(() => {
        messageButton.style.display = "none"
    }, 10000)
})

button.addEventListener("click", ()=> {
    messageButton.style.display = "none"
})
