document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".feedback-form");
    const messageDiv = document.getElementById("feedback-message");
  
    form.addEventListener("submit", function (e) {
      e.preventDefault();  // Prevent default form submission
  
      // Simulate successful submission
      messageDiv.textContent = "Thank you for your feedback!";
      messageDiv.style.display = "block";
  
      // Clear the form
      form.reset();
  
      // Hide the message after 3 seconds
      setTimeout(() => {
        messageDiv.style.display = "none";
      }, 3000);
    });
  });