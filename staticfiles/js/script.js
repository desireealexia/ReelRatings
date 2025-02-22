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

document.addEventListener('DOMContentLoaded', function () {
  const stars = document.querySelectorAll('.star');
  
  stars.forEach(star => {
      star.addEventListener('mouseover', function () {
          this.style.color = 'gold';
          let prevSibling = this.previousElementSibling;
          while (prevSibling) {
              prevSibling.style.color = 'gold';
              prevSibling = prevSibling.previousElementSibling;
          }
      });
      
      star.addEventListener('mouseout', function () {
          stars.forEach(s => s.style.color = '#ddd');
      });
  });
});
