
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".bi.bi-three-dots").forEach(function (button) {
        button.addEventListener('click', function (event) {
            const menu = this.nextElementSibling;
            menu.classList.toggle('open');
            event.stopPropagation();
        });
    });

    window.addEventListener('click', function() {
        closeAllMenus();
    });


    function closeAllMenus() {
        document.querySelectorAll('.menu').forEach(function(menu) {
            menu.classList.remove('open');
        });
    }


});
