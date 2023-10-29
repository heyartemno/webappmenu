let tg = window.Telegram.WebApp;

tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#2cab37';

let item = "";
//const counters = document.querySelectorAll('[counter_wrapper]')


let btn1 = document.getElementById("btn1");
let btn2 = document.getElementById("btn2");
let btn3 = document.getElementById("btn3");
let btn4 = document.getElementById("btn4");
let btn5 = document.getElementById("btn5");
let btn6 = document.getElementById("btn6");

//counter_wrapper.addEventListener('click', function (event) {

//    let counter;
    // Проверка клика строго по кнопкам Плис или Минус
//    if (event.target.dataset.action === 'plus' || event.target.dataset.action === 'minus') {
        // Находим обертку счетчика
//        // Находим див с числом счетчика
//        counter = counterWrapper.querySelector('[data-counter]');
//    }
    // Проверяем элемент является ли он Плюс
//    if (event.target.dataset.action === 'plus') {
//        counter.innerText = ++counter.innerText;
//    }
    // Проверяем элемент является ли он Минус
//    if (event.target.dataset.action === 'minus') {
//       if (parseInt(counter.innerText) > 1){
//            counter.innerText = --counter.innerText;
//        }
//    }
//    })
//};

btn1.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    }
    else {
        tg.MainButton.setText("Товар добавлен в корзину!")
        item = "1";
        tg.MainButton.show();
    }
});

btn2.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    }
    else {
        tg.MainButton.setText("Товар добавлен в корзину!")
        item = "2";
        tg.MainButton.show();
    }
});

btn3.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    }
    else {
        tg.MainButton.setText("Товар добавлен в корзину!")
        item = "3";
        tg.MainButton.show();
    }
});

btn4.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    }
    else {
        tg.MainButton.setText("Товар добавлен в корзину!")
        item = "4";
        tg.MainButton.show();
    }
});

btn5.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    }
    else {
        tg.MainButton.setText("Товар добавлен в корзину!")
        item = "5";
        tg.MainButton.show();
    }
});

btn6.addEventListener("click", function(){
    if (tg.MainButton.isVisible) {
        tg.MainButton.hide();
    }
    else {
        tg.MainButton.setText("Товар добавлен в корзину!")
        item = "6";
        tg.MainButton.show();
    }
});

Telegram.WebApp.onEvent("mainButtonClicked", function(){
    tg.sendData(item);
});