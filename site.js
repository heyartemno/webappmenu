
addEventListener('click', function (event) {

    let counter;
    // Проверка клика строго по кнопкам Плис или Минус
    if (event.target.dataset.action === 'plus' || event.target.dataset.action === 'minus') {
        // Находим обертку счетчика
        const counterWrapper = event.target.closest('.counter_wrapper');
        // Находим див с числом счетчика
        counter = counterWrapper.querySelector('[data-counter]');
    }
    // Проверяем элемент является ли он Плюс
    if (event.target.dataset.action === 'plus') {
        counter.innerText = ++counter.innerText;
    }
    // Проверяем элемент является ли он Минус
    if (event.target.dataset.action === 'minus') {
        if (parseInt(counter.innerText) > 1){
            counter.innerText = --counter.innerText;
        }
    }
});