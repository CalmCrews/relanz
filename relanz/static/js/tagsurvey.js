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
    const nooing = document.getElementById("type_second_afternoon")
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


window.addEventListener("load", () => {
    const tag_lists = ["morning", "afternoon", "evening", "inside", "outside", "solo", "group", "static", "dynamic"];
    const isClickedAboutTime = [false, false, false];
    let handleTime;
    for (let i=0; i<tag_lists.length; i++) {
        const id = `tags_list_${tag_lists[i]}`;
        const divId = tag_lists[i] === "morning" ||tag_lists[i] === "afternoon"|| tag_lists[i] === "evening" ? `type_second_${tag_lists[i]}` : `type_third_${tag_lists[i]}`
        const isClicked = document.getElementById(id).dataset.tags === "True";
        console.log(i, divId, isClicked)
        if (isClicked) {
            if (divId.includes("third")) {
                document.getElementById(divId).click();
                console.log(document.getElementById(divId));
            } else {
                switch (tag_lists[i]) {
                    case "morning":
                        isClickedAboutTime[0] = true;
                        break;
                    case "afternoon":
                        isClickedAboutTime[1] = true;
                        break;
                    case "evening":
                        isClickedAboutTime[2] = true;
                        handleTime = String(isClickedAboutTime.filter((boolean)=>boolean).length) === "3";
                        break;
                }
            }
        }
        if (isClickedAboutTime.length === 3) {
            document.getElementById("type_second_anytime").click();
        } else {
            isClickedAboutTime.forEach((value, index)=>{
                if (Boolean(value)) {
                    document.getElementById(`type_second_${tag_lists[index]}`).click();
                }
            })
        }        
    }
});