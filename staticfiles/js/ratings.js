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
  