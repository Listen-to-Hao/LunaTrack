document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Me.js Loaded");

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

    // 🌸 绑定分类按钮，动态加载帖子
    document.querySelectorAll(".tab-btn").forEach(button => {
        button.addEventListener("click", function () {
            document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            const postType = this.dataset.target; // 获取帖子类型（created, liked, commented, collected）
            fetchPosts(postType);
        });
    });

    // 🌸 获取帖子数据并更新页面
    function fetchPosts(postType) {
        fetch(`/users/me/posts/?type=${postType}`)
            .then(response => response.json())
            .then(data => {
                const postContent = document.querySelector(".post-content");
                postContent.innerHTML = ""; // 清空帖子区域

                if (data.posts.length === 0) {
                    postContent.innerHTML = `<p class="empty-posts">🌸 No posts found in ${postType}.</p>`;
                    return;
                }

                data.posts.forEach(post => {
                    postContent.innerHTML += generatePostHTML(post);
                });
            })
            .catch(error => console.error("❌ Error fetching posts:", error));
    }

    // 🌸 生成单个帖子 HTML 结构
    function generatePostHTML(post) {
        return `
            <div class="post-card" id="post-${post.id}">
                <div class="post-header">
                    <img src="${post.author_avatar}" class="post-avatar">
                    <span class="post-author">${post.author}</span>
                    <span class="post-date">${post.created_at}</span>
                </div>

                <p class="post-inner-content">${post.content}</p>

                ${post.image ? `<img src="${post.image}" class="post-image">` : ""}

                <div class="post-actions">
                    <button class="like-btn" data-post-id="${post.id}">❤️ ${post.likes}</button>
                    <button class="comment-btn" data-post-id="${post.id}">💬 ${post.comments_count}</button>
                    <button class="collect-btn" data-post-id="${post.id}">⭐ ${post.collections}</button>
                    ${post.is_author ? `<button class="btn btn-danger delete-post-btn" data-post-id="${post.id}">🗑️ Delete</button>` : ""}
                </div>

                <div class="comment-section" id="comments-${post.id}" style="display: none;">
                    <div class="comment-list">
                        ${post.comments.map(comment => `
                            <div class="comment" id="comment-${comment.id}">
                                <img src="${comment.avatar}" class="comment-avatar">
                                <div>
                                    <span class="comment-author">${comment.user}</span>: 
                                    <p class="comment-text">${comment.text}</p>
                                </div>
                                ${comment.is_author ? `<button class="btn btn-danger delete-comment-btn" data-comment-id="${comment.id}">Delete</button>` : ""}
                            </div>
                        `).join("")}
                    </div>
                    <div class="comment-input-container">
                        <input type="text" class="comment-input" data-post-id="${post.id}" placeholder="Write a comment...">
                        <button class="submit-comment-btn" data-post-id="${post.id}">Submit</button>
                    </div>
                </div>
            </div>
        `;
    }

    // 🌸 事件委托，处理点赞、收藏、评论等操作
    document.addEventListener("click", function (event) {
        const target = event.target;

        // ❤️ 点赞
        if (target.closest(".like-btn")) {
            const postId = target.dataset.postId;
            fetch(`/users/posts/${postId}/like/`, {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    target.innerHTML = `❤️ ${data.likes}`;
                } else {
                    alert("❌ Failed to like the post!");
                }
            })
            .catch(error => console.error("❌ Fetch Error:", error));
        }

        // 🔖 收藏
        if (target.closest(".collect-btn")) {
            const postId = target.dataset.postId;
            fetch(`/users/posts/${postId}/collect/`, {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    target.innerHTML = `🔖 ${data.collections}`;
                } else {
                    alert("❌ Failed to collect the post!");
                }
            })
            .catch(error => console.error("❌ Fetch Error:", error));
        }

        // 💬 展开评论区
        if (target.closest(".comment-btn")) {
            const postId = target.dataset.postId;
            const commentSection = document.getElementById(`comments-${postId}`);
            if (commentSection) {
                commentSection.style.display = commentSection.style.display === "none" ? "block" : "none";
            }
        }

        // ✍️ 提交评论
        if (target.closest(".submit-comment-btn")) {
            const postId = target.dataset.postId;
            const commentInput = document.querySelector(`.comment-input[data-post-id="${postId}"]`);
            const commentText = commentInput.value.trim();

            if (!commentText) {
                alert("❌ Comment cannot be empty!");
                return;
            }

            fetch(`/users/posts/${postId}/comment/`, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken() 
                },
                body: `content=${encodeURIComponent(commentText)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const commentList = document.querySelector(`#comments-${postId} .comment-list`);
                    commentList.innerHTML += `
                        <div class="comment" id="comment-${data.comment.id}">
                            <span class="comment-author">${data.comment.user}</span>: 
                            <span class="comment-content">${data.comment.text}</span>
                            <button class="btn btn-danger delete-comment-btn" data-comment-id="${data.comment.id}">🗑️ Delete</button>
                        </div>`;
                    commentInput.value = "";
                } else {
                    alert("❌ Failed to add comment!");
                }
            })
            .catch(error => console.error("❌ Fetch Error:", error));
        }

        // 🗑️ 删除帖子
        if (target.closest(".delete-post-btn")) {
            const postId = target.dataset.postId;
            if (confirm("Are you sure you want to delete this post?")) {
                fetch(`/users/me/delete-post/${postId}/`, {
                    method: "POST",
                    headers: { "X-CSRFToken": getCSRFToken() }
                })
                .then(() => {
                    document.getElementById(`post-${postId}`).remove();
                })
                .catch(error => console.error("❌ Fetch Error:", error));
            }
        }

        // 🗑️ 删除评论
        if (target.closest(".delete-comment-btn")) {
            const commentId = target.dataset.commentId;
            if (confirm("Are you sure you want to delete this comment?")) {
                fetch(`/users/me/delete-comment/${commentId}/`, {
                    method: "POST",
                    headers: { "X-CSRFToken": getCSRFToken() }
                })
                .then(() => {
                    document.getElementById(`comment-${commentId}`).remove();
                })
                .catch(error => console.error("❌ Fetch Error:", error));
            }
        }
    });

    // 🌸 绑定 "Edit 个人信息" 按钮
    const editButton = document.querySelector(".edit-profile");
    const editModal = document.getElementById("editProfileModal");

    if (editButton && editModal) {
        let modalInstance = new bootstrap.Modal(editModal);
        editButton.addEventListener("click", function () {
            modalInstance.show();
        });

        // 🌸 绑定 "保存个人信息" 按钮
        const saveButton = document.querySelector("#editProfileForm button[type='submit']");
        if (saveButton) {
            saveButton.addEventListener("click", function (event) {
                event.preventDefault();
                const form = document.getElementById("editProfileForm");
                if (!form) {
                    console.error("❌ Edit form not found!");
                    return;
                }

                let formData = new FormData(form);
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
        }
    }
    
    // 🌸 绑定 "Edit 健康信息" 按钮
    const healthEditButton = document.querySelector(".edit-health");
    const healthEditModal = document.getElementById("editHealthModal");

    if (healthEditButton && healthEditModal) {
        let healthModalInstance = new bootstrap.Modal(healthEditModal);
        healthEditButton.addEventListener("click", function () {
            healthModalInstance.show();
        });

        // 🌸 绑定 "保存健康信息" 按钮
        const saveHealthButton = document.querySelector("#editHealthForm button[type='submit']");
        if (saveHealthButton) {
            saveHealthButton.addEventListener("click", function (event) {
                event.preventDefault();
                const form = document.getElementById("editHealthForm");

                fetch("/users/me/edit-health/", {
                    method: "POST",
                    body: new FormData(form),
                    headers: { "X-CSRFToken": getCSRFToken() }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("✅ Health info updated successfully!");
                        healthModalInstance.hide();
                        location.reload();
                    } else {
                        alert("❌ Error updating health info!");
                        console.error("❌ Update Error:", data.errors);
                    }
                })
                .catch(error => console.error("❌ Fetch Error:", error));
            });
        }
    }

    // 🌸 页面加载时默认加载 "Created" 版块
    fetchPosts("created");
});
