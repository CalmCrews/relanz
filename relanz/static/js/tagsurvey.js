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

function setBackgroundColor(tagId, color) {
    const tag = document.getElementById(`${tagId}`);
    tag.style.backgroundColor = `${color}`;
}
function mouseOverFunc () {
    setBackgroundColor(obj.id, "#D0E0FF")
}
function mouseLeaveFunc () {
    setBackgroundColor(obj.id, "#FFF")
}

function selectMyTag(obj) {
    const inputId = obj.id.split("_").pop();
    const selectBoolean = document.getElementById(inputId).value === ""

    if (inputId === "anytime") {
        // 클릭이 되면 true 아님 false
        const isCLicked = document.getElementById(inputId).value !== "";

        if (!isCLicked) {
            // value가 비어있으면, 클릭이 안되면
            // 이젠 클릭된 상태임.

            document.getElementById(inputId).value = inputId;
            obj.style.backgroundColor = "#D0E0FF";

            // 클릭으로 가자 값이 있으면 눌러야함
            const shouldIClick_morning = document.getElementById("morning").value;
            const shouldIClick_nooing = document.getElementById("nooing").value;
            const shouldIClick_evening = document.getElementById("evening").value;

            if (shouldIClick_morning) {
                console.log("shouldIClick_morning :", document.getElementById("morning").value)
                document.getElementById("type_second_morning").click();
                console.log("shouldIClick_morning :", document.getElementById("morning").value)
            }
            if (shouldIClick_nooing) {
                console.log("shouldIClick_nooing", document.getElementById("nooing").value)
                document.getElementById("type_second_nooing").click()
                console.log("shouldIClick_nooing", document.getElementById("nooing").value)
            }
            if (shouldIClick_evening) {
                console.log("shouldIClick_evening", document.getElementById("evening").value )
                document.getElementById("type_second_evening").click()
                console.log("shouldIClick_evening", document.getElementById("evening").value )
            }
            return;

        } else if (isCLicked) {
            document.getElementById(inputId).value = "";
            obj.style.backgroundColor = "#FFF";

            return;
        }
    }

    document.getElementById(inputId).value = document.getElementById(inputId).value === "" ? inputId : ""
    if (selectBoolean && inputId !== "anytime") {
        obj.style.backgroundColor = "#D0E0FF";

    } else if (!selectBoolean) {

        obj.style.backgroundColor = "#FFF"
        obj.addEventListener("mouseover", ()=>{
            setBackgroundColor(obj.id, "#D0E0FF")
        })
        obj.addEventListener("mouseleave", ()=>{
            setBackgroundColor(obj.id, "#FFF")
        })
    }
}


function selectMyTag2(obj, isSelected) {
    if (isSelected) {
        obj.style.backgroundColor = "#FFF";
    } else {
        obj.style.backgroundColor = "#D0E0FF";
        obj.addEventListener("mouseover", mouseOverFunc);
        obj.addEventListener("mouseleave", mouseLeaveFunc);
    }
}

function selectMyTagForVictim(obj) {
    const inputId = obj.id.split("_").pop();
    const selectBoolean = Boolean(document.getElementById(inputId).value);

    document.getElementById(inputId).value = selectBoolean ? "" : inputId;

    console.log(inputId, selectBoolean)
    console.log(document.getElementById(inputId).value)
    if (inputId === "anytime") {
        const shouldIClick_morning = Boolean(document.getElementById("morning").value);
        const shouldIClick_nooing = Boolean(document.getElementById("nooing").value);
        const shouldIClick_evening = Boolean(document.getElementById("evening").value);

        selectMyTag2(document.getElementById("type_second_morning"), !shouldIClick_morning);
        selectMyTag2(document.getElementById("type_second_nooing"), !shouldIClick_nooing);
        selectMyTag2(document.getElementById("type_second_evening"), !shouldIClick_evening);
    }

    selectMyTag2(obj, selectBoolean);
}