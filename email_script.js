document.addEventListener('DOMContentLoaded', function() {
    const revealButtons = document.querySelectorAll('.reveal-btn');

    revealButtons.forEach(button => {
        button.addEventListener('click', function() {
            const answer = this.nextElementSibling;
            answer.style.display = 'inline';
            this.style.display = 'none';
        });
    });
});