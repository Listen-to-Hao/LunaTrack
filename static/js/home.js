document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ Home.js Loaded");

  // Dynamically display the introduction section
  const sections = document.querySelectorAll(".section");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  });

  sections.forEach((section) => {
    observer.observe(section);
  });

  // Feedback form submission
  const feedbackForm = document.querySelector(".feedback-form");
  if (feedbackForm) {
    feedbackForm.addEventListener("submit", function (event) {
      event.preventDefault();
      const formData = new FormData(feedbackForm);

      fetch("", {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": getCSRFToken() },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          const contentType = response.headers.get("content-type");
          if (!contentType || !contentType.includes("application/json")) {
            throw new TypeError("Response is not JSON");
          }
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            alert("Thank you for your feedback!");
            window.location.reload();  // Refresh the page
          } else {
            alert("Error submitting feedback: " + JSON.parse(data.error));  // Display form error message
          }
        })
        .catch((error) => {
          console.error("❌ Error:", error);
          alert("An error occurred. Please try again.");
        });
    });
  }

  // Get CSRF Token
  function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie) {
      document.cookie.split(";").forEach((cookie) => {
        let [name, value] = cookie.trim().split("=");
        if (name === "csrftoken") {
          cookieValue = value;
        }
      });
    }
    return cookieValue;
  }
});