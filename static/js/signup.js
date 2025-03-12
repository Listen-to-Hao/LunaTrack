document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("signupForm");
    const fields = form.querySelectorAll("input, select, textarea");

    form.addEventListener("submit", function (event) {
        let valid = true;

        fields.forEach(field => {
            let errorDiv = field.closest(".mb-3").querySelector(".error-message");

            if (!field.value.trim()) {
                errorDiv.textContent = `⚠️ ${field.name.replace("_", " ")} is required.`;
                field.classList.add("error");
                valid = false;
            } else {
                errorDiv.textContent = "";
                field.classList.remove("error");
            }
        });

        if (!valid) event.preventDefault(); // Stop form submission if invalid
    });
    
    fields.forEach(field => {
        field.addEventListener("input", function () {
            let errorDiv = field.closest(".mb-3").querySelector(".error-message");
            if (field.value.trim()) {
                errorDiv.textContent = "";
                field.classList.remove("error");
            }
        });
    });
});
