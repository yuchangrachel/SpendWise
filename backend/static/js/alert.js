function alertFadeOut() {
    setTimeout(() => {
      document.querySelector('.flash-messages').style.display = 'none';
    }, 1000);
}

alertFadeOut();