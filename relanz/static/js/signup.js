const passwordInput = document.getElementById("password")
const rePasswordInput = document.getElementById("re_password")

const idCheckBtn = document.getElementById("username_button")
const sumbitBtn = document.getElementById("submit_input")

let passwordIsFilled = false
let rePasswordIsFilled = false
let passwordIsSame = false

const messageAppearFunc = (id) => {
  const tag = document.getElementById(id)
  tag.classList.remove("hide")
}
const messageDisppearFunc = (id) => {
  const tag = document.getElementById(id)
  tag.classList.add("hide")
}

// 중복확인
const onClickCheckId = async () => {
    const id = document.getElementById("username").value
    if (!id) {
        // 빈 문자열일경우. 혹시 문자열의 형식을 정하면 여기에 정규식 표현으로 필터링도 가능 & 유저 피드백 처리도
        return
    }
    // 여기에다 url을 알려줘~
    const url =`/user/api/identify`
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            id,
          }),
    })

    // 여기에서 백에서 준 데이터 받아 변수에 할당하는 곳!
    const data = await response.json();
    
    const approveMsg = "사용가능한 아이디입니다"
    const rejectMsg = "이미 있는 아이디입니다"

    console.log(data.message)
    console.log(data.message === approveMsg)
    console.log(data.message === rejectMsg)

    if (data.message === approveMsg) {
      const approve_msg = document.getElementById("approve_msg")
      const reject_msg = document.getElementById("reject_msg")
      approve_msg.classList.remove("hide")
      reject_msg.classList.add("hide")
      console.log(approve_msg, reject_msg)
      return
    }
    else if (data.message === rejectMsg) {
      const approve_msg = document.getElementById("approve_msg")
      const reject_msg = document.getElementById("reject_msg")
      approve_msg.classList.add("hide")
      reject_msg.classList.remove("hide")
      console.log(approve_msg, reject_msg)
      return
    }
    return
    // 이후 처리에 따라 아이디 중복 여부를 유저에게 피드백하면 됨!
    // reject_msg approve_msg
}
document.getElementById("username_button").addEventListener("click", onClickCheckId)

// 비밀번호 눈알
passwordInput.addEventListener("keyup", (event)=>{
  const inputValue = event.target.value !== "" ? true : false
  if (inputValue) {
    messageAppearFunc("password_eye")
    passwordIsFilled = inputValue
  } else {
    if (passwordIsFilled === inputValue) {
      return
    }
    messageDisppearFunc("password_eye")
    passwordIsFilled = inputValue
  }
})
// 비밀확인 눈알
rePasswordInput.addEventListener("keyup", (event)=> {
  const inputValue = event.target.value !== "" ? true : false
  if (inputValue) {
    messageAppearFunc("rePasswordEye")
    rePasswordIsFilled = inputValue
  } else {
    if (rePasswordIsFilled === inputValue) {
      return
    }
    messageDisppearFunc("rePasswordEye")
    rePasswordIsFilled = inputValue
  }
})

// 공백방지 함수
function noSpaceForm(obj) { // 공백사용못하게
  var str_space = /\s/;  // 공백체크
  if(str_space.exec(obj.value)) { //공백 체크
      
    obj.value = obj.value.replace(' ',''); // 공백제거
    obj.blur()

    const modal = document.getElementById("modal")
    const block_while_modal = document.getElementById("block_while_modal")

    modal.style.visibility = "visible"
    modal.style.zIndex = "1000"

    block_while_modal.style.visibility = "visible"
    block_while_modal.style.zIndex = "100"

    return false;
  }
// onkeyup="noSpaceForm(this);" onchange="noSpaceForm(this);"
}
function modal_btn_ok() {
  const modal = document.getElementById("modal");
  const block_while_modal = document.getElementById("block_while_modal");
  
  modal.style.visibility = "hidden";
  modal.style.zIndex = "-1";

  block_while_modal.style.visibility = "hidden";
  block_while_modal.style.zIndex = "-1";
}


passwordInput.addEventListener("keyup", (event)=>{
  const passwordInput = document.getElementById("password");
  const rePasswordInput = document.getElementById("re_password");
  const isSame = event.target.value === rePasswordInput.value ? true : false;

  const ok_text = "passwordCheckMsgOk";
  const no_rext = "passwordCheckMsgNo";

  if (event.target.value === "" || rePasswordInput.value === "") {
    messageDisppearFunc(ok_text)
    messageDisppearFunc(no_rext)
    return
  } else {
    if (isSame) {
      messageAppearFunc(ok_text)
      messageDisppearFunc(no_rext)
      return
    }
    if (!isSame) {
      messageAppearFunc(no_rext)
      messageDisppearFunc(ok_text)
      return
    }
  }
})

rePasswordInput.addEventListener("keyup", (event)=>{
  const passwordInput = document.getElementById("password");
  const rePasswordInput = document.getElementById("re_password");
  const isSame = event.target.value === passwordInput.value ? true : false;

  const ok_text = "passwordCheckMsgOk";
  const no_rext = "passwordCheckMsgNo";

  if (event.target.value === "" || passwordInput.value === "") {
    messageDisppearFunc(ok_text)
    messageDisppearFunc(no_rext)
    return
  } else {
    if (isSame) {
      messageAppearFunc(ok_text)
      messageDisppearFunc(no_rext)
      return
    }
    if(!isSame) {
      messageAppearFunc(no_rext)
      messageDisppearFunc(ok_text)
      return
    }
  }
})



function convertPassword(obj) {
  const urlList = obj.src.split("/")
  const staticUrl = urlList[urlList.length -1]

  const openEne = "eye.png";
  const closeEye = "closeEye.png";

  const id = obj.id;
  const inputId = id === "pw_eye" ? "password" : "re_password";

  if (staticUrl  === closeEye) {
    document.getElementById(inputId).type = "text";
    obj.src = `/static/images/login/${openEne}`
    return;
  }
  else if (staticUrl === openEne) {
    document.getElementById(inputId).type = "password";
    obj.src = `/static/images/login/${closeEye}`
    return;
  }
}




function checkValidEmail(obj) {
  let regex = new RegExp("([!#-'*+/-9=?A-Z^-~-]+(\.[!#-'*+/-9=?A-Z^-~-]+)*|\"\(\[\]!#-[^-~ \t]|(\\[\t -~]))+\")@([!#-'*+/-9=?A-Z^-~-]+(\.[!#-'*+/-9=?A-Z^-~-]+)*|\[[\t -Z^-~]*])");
  const inputText = obj.value;
  const approve_div_email = document.getElementById("approve_div_email");
  const reject_div_email = document.getElementById("reject_div_email");
  if (!inputText){
    // 글자가 아무것도 없으면!
    approve_div_email.style.zIndex = "-1";
    reject_div_email.style.zIndex = "-1";
  }
  else {
    // 값이 있으면!
    const isEmpty = inputText.includes(" ")
    const isEmail = regex.test(inputText)
    if (!isEmpty && isEmail) {
      approve_div_email.style.zIndex = "10";
      reject_div_email.style.zIndex = "-1";
    }
    else {
      approve_div_email.style.zIndex = "-1";
      reject_div_email.style.zIndex = "10";
    }
  }
}