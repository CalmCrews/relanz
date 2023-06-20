console.log("hih")
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
}

document.getElementById("username_button").addEventListener("click", onClickCheckId)