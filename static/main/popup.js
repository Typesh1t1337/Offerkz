document.addEventListener('DOMContentLoaded', function () {

    const openPopupButtons = document.querySelectorAll('.open-popup');

    openPopupButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();


            const popup = document.querySelector('.pop-up')


            popup.classList.add('open');
        });
    });


    const closePopupButtons = document.querySelectorAll('.close-popup');
    closePopupButtons.forEach(button => {
        button.addEventListener('click', function () {
            const popup = this.closest('.pop-up');
            popup.classList.remove('open');
        });
    });


    window.addEventListener('click', function (e) {
        if (e.target.classList.contains('pop-up')) {
            e.target.classList.remove('open');
        }
    });
});
