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
    const message = await response.json()
    console.log(message)
    // 이후 처리에 따라 아이디 중복 여부를 유저에게 피드백하면 됨!
    // reject_msg approve_msg
}

document.getElementById("username_button").addEventListener("click", onClickCheckId)

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

rePasswordInput.addEventListener("keyup", (event)=> {
  const isSame = event.target.value === passwordInput.value ? true : false
  if (isSame) {
    messageAppearFunc("passwordCheckMsg")
    passwordIsSame = isSame
  } else {
    if (passwordIsSame === isSame) {
      return
    }
    messageDisppearFunc("passwordCheckMsg")
    passwordIsSame = isSame
  }
})

// 마우스 클릭했을 때
document.getElementById("submit_input").addEventListener("mouseover", (event)=>{
  const tag = document.getElementById("submit_input")
  tag.style.backgroundColor = "#3F80FC"
})
document.getElementById("submit_input").addEventListener("mouseleave", (event)=>{

})


idCheckBtn.addEventListener("mouseleave", (event)=>{
  console.log(" 벗어남")
  idCheckBtn.classList.remove("mouse-over");
})