// static/js/crosswords.js

document.addEventListener('DOMContentLoaded', () => {

    const grid = document.querySelector('.crosswords__grid');
    const revealBtn = document.querySelector('.crosswords__reveal');
  
    grid.addEventListener('click', (e) => {
      const cell = e.target.closest('td');
      if (cell.hasAttribute('data-letter')) {
        cell.setAttribute('revealed', true);
        cell.textContent = cell.dataset.letter;
      }
    });
  
    revealBtn.addEventListener('click', () => {  
      grid.querySelectorAll('td[data-letter]').forEach(cell => {
        cell.setAttribute('revealed', true);
        cell.textContent = cell.dataset.letter;      
      });
      revealBtn.disabled = true;
    });
  
  });