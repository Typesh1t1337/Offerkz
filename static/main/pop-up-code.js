document.addEventListener('DOMContentLoaded',function (){
    const openPopupButton = document.getElementById('open-popup');
    const popup = document.getElementById('popup');
    const closePopupButton = document.getElementById('pop-up-close');


    openPopupButton.addEventListener('click',function(){
       popup.classList.add('open');
    });


    closePopupButton.addEventListener('click',function (){
        popup.classList.remove('open')
    })

});