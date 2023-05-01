let slidesParentDiv = document.querySelector('.slides');
let slides = document.querySelectorAll('.slide');
let currentSlide = document.querySelector('.slide.show');
/* -------------------------------------------------------------------------- */
var slideCounter = document.querySelector('.counter');
var leftBtn = document.querySelector('#left-btn');
var rightBtn = document.querySelector('#right-btn');
/* -------------------------------------------------------------------------- */
let presentationArea = document.querySelector('#presentation-area');
var fullScreenBtn = document.querySelector('#full-screen');
var smallScreenBtn = document.querySelector('#small-screen');
/* -------------------------------------------------------------------------- */
var screenStatus   = false;
var currentSlideNo = 1;
var totalSides     = 0;
/* -------------------------------------------------------------------------- */
leftBtn       .addEventListener('click', moveToLeftSlide);
rightBtn      .addEventListener('click', moveToRightSlide);
fullScreenBtn .addEventListener('click', fullScreenMode);
smallScreenBtn.addEventListener('click', smallScreenMode);
/* -------------------------------------------------------------------------- */
function moveToLeftSlide() {
    var tempSlide = currentSlide;
    currentSlide = currentSlide.previousElementSibling;
    tempSlide.classList.remove('show');
    currentSlide.classList.add('show');
}
function moveToRightSlide() {
    var tempSlide = currentSlide;
    currentSlide = currentSlide.nextElementSibling;
    tempSlide.classList.remove('show');
    currentSlide.classList.add('show');
}
/* -------------------------------------------------------------------------- */
function fullScreenMode() {
    presentationArea.classList.add('full-screen');
    fullScreenBtn.classList.remove('show');
    smallScreenBtn.classList.add('show');
    screenStatus = true;
}
function smallScreenMode() {
    presentationController.classList.remove('full-screen');
    fullScreenBtn.classList.add('show');
    smallScreenBtn.classList.remove('show');
    screenStatus = false;
}
function hideLeftButton() {
    if(currentSlideNo^true) {
        toLeftBtn.classList.add('show');
    } else {
        toLeftBtn.classList.remove('show');
    }
}
function hideRightButton() {
    if(currentSlideNo^totalSides) {
        toRightBtn.classList.add('show');
    } else {
        toRightBtn.classList.remove('show');
    }
}