let isInitialLoad = true;
let number = 1;
let isRequestPending = false;

let testNum = 1;

const loadingTag = document.getElementById("loading_img_div");
const div_end = document.getElementById("div_end");


async function makeRequest(url) {
  const resultData = [];
  if (isRequestPending) {
    return; // 요청이 진행 중인 경우 함수 실행 중단
  }
  isRequestPending = true;

  try {
    loadingTag.classList.remove("hide")
    const response = await fetch(url);
    const data = await response.json();



    data.forEach(element => {
      const obj = {
        imgUrl : element.urls.raw,
        atagUrl : element.urls.raw,
      }
      resultData.push(obj);
    });

    // 응답 처리 로직
    ++testNum

  } catch (error) {
    // 에러 처리 로직
  } finally {
    isRequestPending = false;
  }

  loadingTag.classList.add("hide")

  console.log(testNum)

  if ( testNum === 4 ) {
    div_end.style.backgroundColor = "#D0E0FF"
    console.log(testNum)
    observer.disconnect()
  }
  //   const resultData = [
  //     "http://",
  //     "http://",
  //     "http://",

  //     "http://",
  //     "http://",
  //     "http://",

  //     "http://",
  //     "http://",
  //     "http://",
  // ]
  return resultData
}

const getUrl = async () => {
    // 여기에 백엔드 url 적어주삼요r1eNaU0kipEVvTaIpS0wNwzka5GLv5rdG6Iut6tQ";
    const url = ``;
    const resultData = await makeRequest(url);
    
    return resultData;
} 

function makeImageDiv(imageUrlList) {
  const outerDiv = document.getElementById("images_box_div");

  if (imageUrlList === undefined) {
    return
  }
  if (imageUrlList.length === 0) {
    return
  }

  console.log("imageUrlList :", imageUrlList)

  for (let i=0; i<imageUrlList.length; i++) {
    const a_tag = document.createElement("a");
    const div_tag = document.createElement("div");
    const img_tag = document.createElement("img");

    // 여기에 url 입력
    a_tag.href = imageUrlList[i].atagUrl;
    
    img_tag.src = imageUrlList[i].imgUrl

    a_tag.classList.add("images-box-single");
    div_tag.classList.add("images-box-single");
    img_tag.classList.add("images-box-img");

    div_tag.appendChild(img_tag);
    a_tag.appendChild(div_tag);

    outerDiv.appendChild(a_tag);
  }
}

async function handleIntersection(entries, observer) {
  if (isInitialLoad) {
      return; // 이미 throttle 중이라면 함수 실행을 중지합니다.
  }
  
  for (let entry of entries) {
      console.log("이미지 투척짱!")
      if (entry.intersectionRect) {
          const listUrl = await getUrl();
          makeImageDiv(listUrl);
      }   
  }
}
  
// Create an instance of the Intersection Observer
const options = {
root: null,
rootMargin: '0px',
threshold: 1, // Adjust this value as needed
};
  
const observer = new IntersectionObserver(handleIntersection, options);

// Find the element representing the end of the web page
const targetElement = document.querySelector('#see_full_go_next');

// Start observing the target element
if (targetElement) {
observer.observe(targetElement);
}

window.addEventListener("load", () => {
    isInitialLoad = false;
});