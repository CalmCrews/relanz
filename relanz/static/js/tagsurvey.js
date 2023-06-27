const changePage = function(obj) {
    const pageIndex = String(obj.dataset.pageindex);

    const title = document.getElementById("title");
    const sub_title = document.getElementById("sub_title");

    switch (pageIndex) {
        case "1":
            title.innerText = "당신을 위한 추천에 반영하기 위해"
            sub_title.innerText = "하루 중 어떤 시간대에 스트레스 해소 활동을\n하고 싶으신가요?"

            document.getElementById("select_type_first").style.zIndex = "-1";
            document.getElementById("select_type_second").style.zIndex = "10";
            obj.dataset.pageindex = "2";
            break;
        case "2":
            sub_title.innerText = "원하는 스트레스 해소 활동의\n키워드를 선택해 주세요!"

            document.getElementById("select_type_second").style.zIndex = "-1";
            document.getElementById("select_type_third").style.zIndex = "10";
            obj.dataset.pageindex = "3";
            break;
        case "3":
            document.getElementById("real_submit_btn").click();
            break;
    }
}

function selectMyTag(obj) {
    const isClicked = String(obj.dataset.isclicked) === "1" ? true : false;

    const inputId = obj.id.split("_").pop();
    const tag = document.getElementById(inputId)


    if (isClicked) {
        obj.classList.remove("clicked-change-color");
        obj.dataset.isclicked = "0"

        tag.value = "";
    }
    else {
        obj.classList.add("clicked-change-color");
        obj.dataset.isclicked =  "1"

        tag.value = inputId;
    }
}


function selectMyTag_ver2 (obj) {
    const isClicked = String(obj.dataset.isclicked) === "1" ? true : false;

    const inputId = obj.id.split("_").pop();
    const tag = document.getElementById(inputId)

    const morning = document.getElementById("type_second_morning")
    const nooing = document.getElementById("type_second_nooing")
    const evening = document.getElementById("type_second_evening")
    const anytime = document.getElementById("type_second_anytime")

    if (inputId === 'anytime') {
        if (String(morning.dataset.isclicked) === "1") {
            morning.click()
        }
        if (String(nooing.dataset.isclicked) === "1") {
            nooing.click()
        }
        if (String(evening.dataset.isclicked) === "1") {
            evening.click()
        }
    }

    if (isClicked) {
        obj.classList.remove("clicked-change-color");
        obj.dataset.isclicked = "0"

        tag.value = "";
    }
    else {
        if (String(anytime.dataset.isclicked) === "1" && inputId !== 'anytime') {
            anytime.click()
        }

        obj.classList.add("clicked-change-color");
        obj.dataset.isclicked =  "1"

        tag.value = inputId;

        const morning_boolean = String(morning.dataset.isclicked) === "1";
        const nooing_boolean = String(nooing.dataset.isclicked) === "1";
        const evening_boolean = String(evening.dataset.isclicked) === "1";

        if (morning_boolean && nooing_boolean && evening_boolean && inputId !== 'anytime') {
            morning.click()
            nooing.click()
            evening.click()
            anytime.click()
        }
        
    }
}