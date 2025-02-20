// Initialize toast when the page is loaded
document.addEventListener("DOMContentLoaded", function () {
    var toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(function (toastElement) {
      var toast = new bootstrap.Toast(toastElement, {
        delay: 5000 // Adjust delay to how long the toast should be visible
      });
      toast.show();
    });
  });

// Save scroll position before navigating to the next/previous page
function saveScrollPosition() {
  sessionStorage.setItem("scrollPosition", window.scrollY);
}

// Restore scroll position when the page loads
function restoreScrollPosition() {
  let scrollPosition = sessionStorage.getItem("scrollPosition");
  if (scrollPosition) {
      window.scrollTo(0, scrollPosition);
  }
}

// Trigger scroll restore on page load
window.onload = restoreScrollPosition;

// Trigger scroll save before navigating to the next or previous page
document.querySelectorAll('.pagination a').forEach(function(link) {
  link.addEventListener('click', saveScrollPosition);
});
