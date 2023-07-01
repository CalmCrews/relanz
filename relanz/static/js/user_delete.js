function submitDeleteUser() {
    document.getElementById("screen_block_div").style.zIndex = "5";
    document.getElementById("good_pw").style.zIndex = "10";
    
}

function concealDeleteUser () {
    document.getElementById("password_real").value = "";
    document.getElementById("screen_block_div").style.zIndex = "-1";
    document.getElementById("good_pw").style.zIndex = "-1";
}

function clickRealSubmit () {
    document.getElementById("real_submit_btn").click();
}

function wrongPasswordBtn () {
    document.getElementById("bad_pw").style.zIndex = "-1";
}