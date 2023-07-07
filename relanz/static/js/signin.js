const warning_btn = document.getElementById("warning_btn")
const warning_user_div = document.getElementById("warning_user_div")

if (warning_btn) {
    warning_btn.addEventListener("click", ()=>{
        warning_user_div.classList.add("hide")
    })
}