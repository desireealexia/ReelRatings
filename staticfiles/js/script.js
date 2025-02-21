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