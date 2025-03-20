document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Record.js Loaded");

    let modalElement = document.getElementById("recordModal");
    let searchModalElement = document.getElementById("searchModal");

    if (!modalElement) {
        console.error("❌ recordModal not found!");
        return;
    }

    let modal = new bootstrap.Modal(modalElement);
    let searchModal = searchModalElement ? new bootstrap.Modal(searchModalElement) : null;
    let recordForm = document.getElementById("recordForm");
    let recordId = null;

    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie) {
            document.cookie.split(";").forEach(cookie => {
                let [name, value] = cookie.trim().split("=");
                if (name === "csrftoken") {
                    cookieValue = value;
                }
            });
        }
        return cookieValue;
    }

    // Ensure End Date is not earlier than Start Date
    let startDateInput = document.getElementById("start_date");
    let endDateInput = document.getElementById("end_date");

    if (startDateInput && endDateInput) {
        startDateInput.addEventListener("change", function () {
            endDateInput.min = startDateInput.value;
        });
    }

    // Reset form
    function resetForm() {
        document.getElementById("recordForm").reset();
    }

    // Bind "Add" button
    let addButton = document.querySelector(".add-btn");
    if (addButton) {
        addButton.addEventListener("click", function () {
            recordId = null;
            resetForm();  // 🔥 **Fixing function call error**
            modal.show();
        });
    } else {
        console.error("❌ Add button not found!");
    }

    // Bind "Edit" button
    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function () {
            recordId = button.getAttribute("data-id");
            fetch(`/record/${recordId}/edit/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById("start_date").value = data.start_date;
                        document.getElementById("end_date").value = data.end_date;
                        document.getElementById("blood_volume").value = data.blood_volume;
                        document.getElementById("clotting").value = data.clotting;
                        document.getElementById("mood_swings").value = data.mood_swings;
                        document.getElementById("stress_level").value = data.stress_level;
                        document.getElementById("weight").value = data.weight; // Load weight data
                        document.getElementById("symptom_description").value = data.symptom_description;
                        modal.show();
                    } else {
                        alert("❌ Error loading record!");
                    }
                })
                .catch(error => console.error("❌ Edit Error:", error));
        });
    });

    // Bind "Delete" button
    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function () {
            let recordId = button.getAttribute("data-id");
            fetch(`/record/${recordId}/delete/`, {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let recordCard = document.querySelector(`.record-card[data-id='${recordId}']`);
                    if (recordCard) {
                        recordCard.style.transition = "opacity 0.3s ease-out";
                        recordCard.style.opacity = "0";
                        setTimeout(() => recordCard.remove(), 300);
                    }
                } else {
                    alert("❌ Error deleting record!");
                }
            })
            .catch(error => console.error("❌ Delete Error:", error));
        });
    });

    // Bind "Search" button
    let searchBtn = document.getElementById("search-btn");
    let confirmSearch = document.getElementById("confirmSearch");

    if (searchBtn) {
        searchBtn.addEventListener("click", function () {
            if (searchModal) {
                searchModal.show();
            } else {
                alert("❌ Search modal not found!");
            }
        });
    }

    // Bind "Search Confirm" button
    if (confirmSearch) {
        confirmSearch.addEventListener("click", function () {
            let inputMonth = document.getElementById("searchMonth").value;
            if (!inputMonth) {
                alert("❌ Please select a month!");
                return;
            }

            let records = document.querySelectorAll(".record-card");
            let found = false;
            let firstRecord = null;

            // **Supports both abbreviated and full month names**
            let monthMap = {
                "Jan.": "01", "January": "01", "Feb.": "02", "February": "02",
                "Mar.": "03", "March": "03", "Apr.": "04", "April": "04",
                "May": "05", "Jun.": "06", "June": "06", "Jul.": "07", "July": "07",
                "Aug.": "08", "August": "08", "Sep.": "09", "September": "09",
                "Oct.": "10", "October": "10", "Nov.": "11", "November": "11",
                "Dec.": "12", "December": "12"
            };

            records.forEach(record => {
                let dateElement = record.querySelector(".record-dates");
                if (dateElement) {
                    let dateText = dateElement.textContent.trim();
                    
                    // **New regex to match both full and abbreviated months**
                    let match = dateText.match(/\b([A-Za-z]+\.?) (\d{1,2}), (\d{4})\b/);
                    if (match) {
                        let month = match[1];  // Could be "Jan." or "January"
                        let year = match[3];   // Year
                        let formattedMonth = `${year}-${monthMap[month]}`;

                        if (formattedMonth === inputMonth) {
                            if (!firstRecord) {
                                firstRecord = record; // Record the first matching record
                            }
                        }
                    }
                }
            });

            if (firstRecord) {
                firstRecord.scrollIntoView({ behavior: "smooth", block: "center" });
                found = true;
            }

            if (!found) {
                alert(`❌ No records found for ${inputMonth}`);
            }

            searchModal.hide();
        });
    }

    // Form submission
    recordForm.addEventListener("submit", function (event) {
        event.preventDefault();
        let formData = new FormData(recordForm);
        let url = recordId ? `/record/${recordId}/edit/` : "/record/add/";

        fetch(url, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(" Record saved successfully!");
                modal.hide();

               setTimeout(() => location.reload(), 500);
            } else {
                alert("❌ Error saving record!");
            }
        })
        .catch(error => console.error("❌ Save Error:", error));
    });
});
