
async function clickLikeHeartBtn(obj) {
    const url = obj.dataset.url
    const response = await fetch(url)
    const data = await response.json()

    const {
        isClicked, likeCount
    } = data;

    if (isClicked) {
        document.getElementById("like_count").innerText = likeCount;
        document.getElementById("like_heart_img_div").classList.add("hide");
        document.getElementById("dislike_heart_img_div").classList.remove("hide");
    }
    else {
        document.getElementById("like_count").innerText = likeCount;
        document.getElementById("like_heart_img_div").classList.remove("hide");
        document.getElementById("dislike_heart_img_div").classList.add("hide");
    }
    
}

function clickCancelBtn(obj) {
    document.getElementById("warning_user_div").remove();
}