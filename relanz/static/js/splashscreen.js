function goToHome() {
  window.location.href = "{% url 'main:home' %}";
}

function scrollDiv() {
  const container = document.querySelector(".scrollable-container");
  let items = document.querySelectorAll(".scrollable-item");

  container.scrollTop = items[0].offsetTop;

  const scrollInterval = 2500;

  setInterval(function () {
    const firstItem = items[0];
    if (firstItem.id === "div4") {
      goToHome();
    }
    container.removeChild(firstItem);
    container.appendChild(firstItem);

    console.log("remove!");
    items = document.querySelectorAll(".scrollable-item");
    container.scrollTop = items[0].offsetTop;
  }, scrollInterval);
}

// 페이지 로드 시 스크롤 이벤트 함수 호출
window.addEventListener("load", scrollDiv);
