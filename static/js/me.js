document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Me.js Loaded");

    // 🌸 切换帖子分类
    document.querySelectorAll(".tab-btn").forEach(button => {
        button.addEventListener("click", function () {
            document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
            document.querySelectorAll(".post-section").forEach(section => section.classList.remove("active"));

            this.classList.add("active");
            document.getElementById(this.dataset.target).classList.add("active");
        });
    });

    // 🌸 绑定 "Edit" 按钮
    const editButton = document.querySelector(".edit-profile");
    const editModal = document.getElementById("editProfileModal");

    if (!editButton || !editModal) {
        console.error("❌ Edit button or modal not found!");
        return;
    }

    let modalInstance = new bootstrap.Modal(editModal);
    editButton.addEventListener("click", function () {
        modalInstance.show();
    });

    // 🌸 获取 CSRF Token
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

    // 🌸 绑定 "保存更改" 按钮
    const saveButton = document.querySelector("#editProfileForm button[type='submit']");
    if (!saveButton) {
        console.error("❌ Save button not found!");
        return;
    }

    saveButton.addEventListener("click", function (event) {
        event.preventDefault();
        const form = document.getElementById("editProfileForm");
        if (!form) {
            console.error("❌ Edit form not found!");
            return;
        }

        let formData = new FormData(form);

        // 🌸 处理未修改的文件字段
        let avatarInput = document.getElementById("avatar");
        if (avatarInput.files.length === 0) {
            formData.delete("avatar");
        }

        fetch("/users/me/edit/", {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("✅ Profile updated successfully!");
                modalInstance.hide();
                location.reload();
            } else {
                alert("❌ Error updating profile!");
                console.error("❌ Update Error:", data.errors);
            }
        })
        .catch(error => console.error("❌ Fetch Error:", error));
    });
});
