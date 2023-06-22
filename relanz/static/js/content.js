function selectLiYear(obj) {
    const value = obj.value

    const setValueDiv = document.getElementById("select_born_year")
    const hidden_birth = document.getElementById("hidden_birth")
    setValueDiv.innerText = `${value}년`
    hidden_birth.value = value

    const up_circle_name = "check_circle_up.png";
    const showBirthArrow = document.getElementById("showBirthArrow")
    showBirthArrow.src = `/static/icons/${up_circle_name}`
    document.getElementById("select_li_div").style.zIndex = -1
    document.getElementById("select_li_div").style.visibility = "hidden"
}


function makeSelectLiTag(year) {
    const liTag = document.createElement("li")
    liTag.value = year
    liTag.innerText = `${year}년`

    liTag.style.listStyle = "none"
    liTag.style.width = "250px"
    liTag.style.height = "20px"
    liTag.style.color = "#494949"
    liTag.style.fontFamily = "Pretendard"
    liTag.style.fontWeight = "300"
    liTag.style.paddingLeft = "1.5em"
    liTag.style.paddingBottom = "1.5em"
    liTag.style.paddingTop = "0.3em"


    liTag.addEventListener('mouseover', function() {
        liTag.style.cursor = "pointer"
        liTag.style.background = "#D0E0FF"
    })
    liTag.addEventListener('mouseleave', function() {
        liTag.style.cursor = "pointer"
        liTag.style.background = "#FFF"
    })
    liTag.addEventListener("click", function() {
        selectLiYear(this);
    })
    
    return liTag;
}

function appendSelectLiTag() {
    const nowyear = new Date().getFullYear()
    const endYear = nowyear - 80

    for (let i=nowyear; i>=endYear; i--) {
        const liTag = makeSelectLiTag(i)
        const select_li_div = document.getElementById("select_li_div")
        select_li_div.appendChild(liTag)
    }
}


appendSelectLiTag()
document.getElementById("select_li_div").style.zIndex = -1
document.getElementById("select_li_div").style.visibility = "hidden"

function showBirthYear (obj) {
    const list = obj.src.split("/");
    const fileName = list[list.length -1]

    const up_circle_name = "check_circle_up.png";
    const down_circle_name = "check_circle_down.png";

    console.log(fileName)
    if (fileName === up_circle_name) {
        obj.src = `/static/icons/${down_circle_name}`
        
        document.getElementById("select_li_div").style.zIndex = 1
        document.getElementById("select_li_div").style.visibility = "visible"
        return
    }
    if (fileName === down_circle_name) {
        obj.src = `/static/icons/${up_circle_name}`
        document.getElementById("select_li_div").style.zIndex = -1
        document.getElementById("select_li_div").style.visibility = "hidden"
        return
    }
}


function selectOnlyOneGenderForMan (obj) {
    const activeId = obj.value === "남자" ? "sex_male" : "sex_female"

    if (activeId === "sex_male") {
        const sex_male_tag = document.getElementById("sex_male")
        const sex_female_tag = document.getElementById("sex_female")

        console.log(sex_male_tag)
        sex_male_tag.style.backgroundColor = "#D0E0FF";

        sex_female_tag.style.backgroundColor = "#FFF";

        document.getElementById("sex_value").value = "male";
        return
    }
}

function selectOnlyOneGenderForWoman (obj) {
    const activeId = obj.value === "남자" ? "sex_male" : "sex_female"

    if (activeId === "sex_female") {
        const sex_male_tag = document.getElementById("sex_male")
        const sex_female_tag = document.getElementById("sex_female")

        sex_female_tag.style.backgroundColor = "#D0E0FF"

        sex_male_tag.style.backgroundColor = "#FFF";

        document.getElementById("sex_value").value = "female";
        return
    }
}