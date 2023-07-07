// document.getElementById(`${color}_${num}`).src = ``


const contentDiv_1 = document.getElementById("linebreaks_fix_1");
const contentDiv_2 = document.getElementById("linebreaks_fix_2");

const paragraphs_1 = contentDiv_1.innerHTML.split("<br>");
const paragraphs_2 = contentDiv_2.innerHTML.split("<br>");
contentDiv_1.innerHTML = "";
contentDiv_2.innerHTML = "";

window.addEventListener('DOMContentLoaded',function() {
    const newDiv = paragraphs_1.filter(word => word !== '')
    newDiv.forEach((paragraph) => {
    const p = document.createElement("p");
    p.innerHTML = paragraph;
    contentDiv_1.appendChild(p);
    });

    const newDi = paragraphs_2.filter(word => word !== '')
    newDi.forEach((paragraph) => {
    const p = document.createElement("p");
    p.innerHTML = paragraph;
    contentDiv_2.appendChild(p);
    });
})

