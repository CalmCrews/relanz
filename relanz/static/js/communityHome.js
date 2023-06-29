let isInitialLoad = true;
let number = 1;
let isRequestPending = false;
let timeouter
let throttle
let newObserver

let testNum = 1;

const loadingTag = document.getElementById("div_end");
const div_end = document.getElementById("div_end");

const delay = (ms) => {
  return new Promise((resolve) =>
  timeouter = setTimeout(() => {
    }, ms)
  );
};

async function makeRequest(url) {
    if (isRequestPending || timeouter) {
      return; // 요청이 진행 중인 경우 함수 실행 중단
    }
  
    isRequestPending = true;

    let data;

    try {
      // loadingTag.classList.remove("hide")
      // const response = await fetch(url);
      // data = await response.json();
      // 응답 처리 로직
      console.log("시작")
      clearTimeout(timeouter)
      timeouter = null
      delay(4000);
      ++testNum

    } catch (error) {
      // 에러 처리 로직
    } finally {
      console.log("끝")
      isRequestPending = false;
    }

    loadingTag.classList.add("hide")

    console.log(testNum)
    if ( testNum === 4 ) {
      console.log(newObserver)
      newObserver.disconnect()
    }

    const resultData = [
      "http://",
      "http://",
      "http://",

      "http://",
      "http://",
      "http://",

      "http://",
      "http://",
      "http://",
  ]
    return resultData
}

const getUrl = async () => {

    // 여기에 백엔드 url 적어주삼요
    const url = ``;

    const resultData = await makeRequest(url);

    return resultData;
} 

function makeImageDiv(imageUrlList) {
    const outerDiv = document.getElementById("images_box_div");

  if (imageUrlList) {}

    for (let i=0; i<imageUrlList.length; i++) {
        const a_tag = document.createElement("a");
        const div_tag = document.createElement("div");
        const img_tag = document.createElement("img");

        // 여기에 url 입력
        a_tag.href = "";
        
        // img_tag.src = "/Users/iin/development/Relanz/relanz/static/images/leein_example.jpeg";
        // img_tag.src = "{% static 'images/leein_example.jpeg' %}"
        img_tag.src = "https://pds.joongang.co.kr/news/component/htmlphoto_mmdata/201808/26/889cec62-8806-4d4c-9e45-b2fe2bfd1f59.jpg"

        a_tag.classList.add("images-box-single");
        div_tag.classList.add("images-box-single");
        img_tag.classList.add("images-box-img");

        div_tag.appendChild(img_tag);
        a_tag.appendChild(div_tag);

        outerDiv.appendChild(a_tag);
    }
}

let isThrottled = false;

async function handleIntersection(entries, observer) {
    if (isThrottled  || isInitialLoad) {
        return; // 이미 throttle 중이라면 함수 실행을 중지합니다.
    }
    
    for (let entry of entries) {
        console.log("이미지 투척짱!")
        if (entry.intersectionRect) {
            const listUrl = await getUrl();
            makeImageDiv(listUrl);
        }   
    }
    
    isThrottled = true;
    clearTimeout(throttle)
    throttle = setTimeout(() => {
        isThrottled = false;
    }, 1000);
}
  
// Create an instance of the Intersection Observer
const options = {
root: null,
rootMargin: '0px',
threshold: 1, // Adjust this value as needed
};
  
const observer = new IntersectionObserver(handleIntersection, options);
newObserver = observer

// Find the element representing the end of the web page
const targetElement = document.querySelector('#see_full_go_next');

// Start observing the target element
if (targetElement) {
observer.observe(targetElement);
}

window.addEventListener("load", () => {
    isInitialLoad = false;
});