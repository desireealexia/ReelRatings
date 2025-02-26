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

  document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star-rating input");
  
    stars.forEach(star => {
        star.addEventListener("change", function () {
            const rating = this.value;
            highlightStars(rating);
        });
    });
  
    function highlightStars(rating) {
        stars.forEach(star => {
            if (star.value <= rating) {
                star.nextElementSibling.classList.add("selected");
            } else {
                star.nextElementSibling.classList.remove("selected");
            }
        });
    }
  });
  