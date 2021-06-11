// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {
    toggleBackToTopButton()
};

function toggleBackToTopButton() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("backTopBtn").style.display = "block";
  } else {
    document.getElementById("backTopBtn").style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function backToTop() {
  document.body.scrollTo({top: 0, behavior: 'smooth'}); // For Safari
  document.documentElement.scrollTo({top: 0, behavior: 'smooth'}); // For Chrome, Firefox, IE and Opera
}
