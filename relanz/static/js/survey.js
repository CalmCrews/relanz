const mentList = [
    [
        "일이 풀리지 않으면 자책부터 하는 편이다.",
        "중요한 문제를 의논할 친구가 없다.",
        "본인이 원하는 것을 명확하게 표현하지 못한다.",
        "일을 해냈을 때 성취감보다 안도감이 든다.",
        "취미 샐활이 일로 느껴져 포기했다.",
        "이루고자 하는 목표가 높다는 말을 자주 듣는다.",
        "칭찬을 듣고 의심해 본 적이 많다.",
    ],
    [
        
    ],
    []
]

function controlPopUp() {
    const pop_up_div = document.getElementById("pop_up_div")
    const index = pop_up_div.dataset.index
    if (index === "-1") {
    const pop_up_div = document.getElementById("pop_up_div")
        pop_up_div.style.zIndex = "10"
        pop_up_div.dataset.index = "10"
    } else {
        pop_up_div.style.zIndex = "-1"
        pop_up_div.dataset.index = "-1"
    }
}

function checkTurnBlue(obj) {
    const isClicked = Boolean(Number(obj.dataset.ischeck))
    if (isClicked) {
        obj.style.backgroundColor = "#FFF"
        obj.dataset.ischeck = "0"
    } else {
        obj.style.backgroundColor = "#D0E0FF"
        obj.dataset.ischeck = "1"
    }
}