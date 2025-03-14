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

    // ✅ 获取 CSRF Token
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

    // ✅ 确保 End Date 不能早于 Start Date
    let startDateInput = document.getElementById("start_date");
    let endDateInput = document.getElementById("end_date");

    if (startDateInput && endDateInput) {
        startDateInput.addEventListener("change", function () {
            endDateInput.min = startDateInput.value;
        });
    }

    // ✅ 重置表单
    function resetForm() {
        document.getElementById("recordForm").reset();
    }

    // ✅ 绑定 "Add" 按钮
    let addButton = document.querySelector(".add-btn");
    if (addButton) {
        addButton.addEventListener("click", function () {
            recordId = null;
            resetForm();  // 🔥 **修复调用错误**
            modal.show();
        });
    } else {
        console.error("❌ Add button not found!");
    }

    // ✅ 绑定 "Edit" 按钮
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
                        document.getElementById("weight").value = data.weight; // 加载体重数据
                        document.getElementById("symptom_description").value = data.symptom_description;
                        modal.show();
                    } else {
                        alert("❌ Error loading record!");
                    }
                })
                .catch(error => console.error("❌ Edit Error:", error));
        });
    });

    // ✅ 绑定 "Delete" 按钮
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

    // ✅ 绑定 "Search" 按钮
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

    // ✅ 绑定 "Search Confirm" 按钮
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

            // 🌟 **支持缩写和完整月份的映射**
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
                    
                    // 🌟 **新的正则表达式匹配完整月份和缩写**
                    let match = dateText.match(/\b([A-Za-z]+\.?) (\d{1,2}), (\d{4})\b/);
                    if (match) {
                        let month = match[1];  // 可能是 "Jan." 或 "January"
                        let year = match[3];   // 年份
                        let formattedMonth = `${year}-${monthMap[month]}`;

                        if (formattedMonth === inputMonth) {
                            if (!firstRecord) {
                                firstRecord = record; // 记录第一条匹配的记录
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

    // ✅ 表单提交
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