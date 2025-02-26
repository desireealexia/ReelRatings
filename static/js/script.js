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

// To access the stars
let stars = document.getElementsByClassName("star");
let output = document.getElementById("output");
let ratingInput = document.getElementById("ratingValue");
 
// Function to update rating
function setRating(n) {
    remove();
    for (let i = 0; i < n; i++) {
        if (n == 1) cls = "one";
        else if (n == 2) cls = "two";
        else if (n == 3) cls = "three";
        else if (n == 4) cls = "four";
        else if (n == 5) cls = "five";
        stars[i].className = "star " + cls;
    }
    output.innerText = "Rating is: " + n + "/5";
    ratingInput.value = n;
}
 
// To remove the pre-applied styling
function remove() {
    let i = 0;
    while (i < 5) {
        stars[i].className = "star";
        i++;
    }
}

// Show more button
function toggleText() {
var dots = document.getElementById("dots");
var moreText = document.getElementById("more-text");
var btnText = document.getElementById("read-more-btn");

if (dots.style.display === "none") {
    // Show the truncated text
    dots.style.display = "inline";
    moreText.style.display = "none";
    btnText.innerHTML = "Read more";
} else {
    // Show the full text
    dots.style.display = "none";
    moreText.style.display = "inline";
    btnText.innerHTML = "Read less";
}
}