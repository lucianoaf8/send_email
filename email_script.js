function revealAnswer(button) {
    const answer = button.nextElementSibling;
    answer.style.display = 'block';
    button.style.display = 'none';
}