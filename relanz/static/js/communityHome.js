
let isInitialLoad = true;
let isRequestPending = false;

const loadingTag = document.getElementById("loading_img_div");
const div_end = document.getElementById("div_end");
const getNumDiv = document.getElementById("images_box_div");
const basicUrl = getNumDiv.dataset.askurl;

const mobileDiv = document.querySelector("#mobile-content"); 

async function makeRequest(url) {
  if (isRequestPending) {
    return; // 요청이 진행 중인 경우 함수 실행 중단
  }
  isRequestPending = true;

  try {
    loadingTag.classList.remove("hide");
    const response = await fetch(url);
    const data = await response.json();
    const parseData = JSON.parse(data)

    const resultData = parseData.map(element => {
      return {
        imgUrl: element.fields.image,
        challenge: element.fields.challenge,
        pk: element.pk,
      }
    });
    console.log(resultData)

    return resultData;
  } catch (error) {
      // 에러 처리 로직
      console.error(error);
      mobileDiv.removeEventListener("scroll", scrollHandler);
  } finally {
    isRequestPending = false;
    isInitialLoad = true;
    loadingTag.classList.add("hide");
  }
}

async function getUrl() {

  const number = getNumDiv.dataset.startnum
  const paramsObj = { page: `${number}`};
  const searchParams = new URLSearchParams(paramsObj);
  const browserLink = document.location.href;
  const browserBasicUrl = browserLink.split("/").slice(0,3).join("/")
  const url = new URL(`${browserBasicUrl}/${basicUrl}`);
  url.search = searchParams.toString();

  const resultData = await makeRequest(url.href);
  getNumDiv.dataset.startnum = Number(number) + 1;
  return resultData;
}

function makeImageDiv(imageUrlList) {
  const outerDiv = document.getElementById("images_box_div");

  if (!imageUrlList || imageUrlList.length === 0) {
    return;
  }

  for (let i = 0; i < imageUrlList.length; i++) {
    const a_tag = document.createElement("a");
    const div_tag = document.createElement("div");
    const img_tag = document.createElement("img");

    const browserLink = document.location.href;
    const browserBasicUrl = browserLink.split("/").slice(0,3).join("/")
    console.log(browserBasicUrl);

    a_tag.href = `${browserBasicUrl}/community/${imageUrlList[i].challenge}/${imageUrlList[i].pk}`;
    img_tag.src = `${browserBasicUrl}/media/${imageUrlList[i].imgUrl}`;

    a_tag.classList.add("images-box-single");
    div_tag.classList.add("images-box-single");
    img_tag.classList.add("images-box-img");

    div_tag.appendChild(img_tag);
    a_tag.appendChild(div_tag);

    outerDiv.appendChild(a_tag);
  }
}

async function handleIntersection(entries, observer) {
  for (let entry of entries) {
    if (entry.isIntersecting) {
      const listUrl = await getUrl();
      makeImageDiv(listUrl);
      observer.unobserve(entry.target);
    }
  }
}

function observeSeeFullGoNext() {
  const targetElement = document.querySelector("#see_full_go_next");
  if (targetElement) {
    const observer = new IntersectionObserver(handleIntersection, {
      root: null,
      rootMargin: "1px",
      threshold: 0.5,
    });
    observer.observe(targetElement);
  }
}

const scrollHandler = () => {
  if (isInitialLoad) {
    observeSeeFullGoNext();
    isInitialLoad = false;
  }
};

mobileDiv.addEventListener("scroll", scrollHandler);
