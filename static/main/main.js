document.querySelectorAll('.footer-faq').forEach(accordion => {
  accordion.querySelectorAll('.faq-box').forEach(item => {
    const header = item.querySelector('.visible_part');
    const content = item.querySelector('.hidden_part');
    const symbol = header.querySelector('.plus');

    header.addEventListener('click', () => {
      const isOpen = content.classList.contains('open');


      accordion.querySelectorAll('.hidden_part').forEach(c => {
        c.classList.remove('open');
        c.previousElementSibling.querySelector('.plus').textContent = '+';
      });

      if (!isOpen) {
        content.classList.add('open');
        header.classList.add('open')
        symbol.textContent = '-';
      } else {
        content.classList.remove('open');
        symbol.textContent = '+';
        header.classList.remove('open')
      }
    });
  });
});


