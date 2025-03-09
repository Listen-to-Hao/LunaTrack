document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ discover.js Loaded");

    let page = 1;
    let searchQuery = "";
    let modal = new bootstrap.Modal(document.getElementById("postModal"));
    let postList = document.getElementById("postList");

    /** ✅ 获取 CSRF Token **/
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

    /** ✅ 加载帖子 **/
    function loadPosts() {
        fetch(`/discover/posts/?page=${page}&q=${searchQuery}`)
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    console.error("❌ Failed to load posts:", data.message);
                    return;
                }

                data.posts.forEach(post => {
                    const postElement = document.createElement("div");
                    postElement.className = "post-card";
                    postElement.innerHTML = `
                        <div class="post-header">
                            <img src="${post.author_avatar}" class="post-avatar">
                            <span class="post-author">${post.author}</span>
                            <span class="post-date">${post.created_at}</span>
                        </div>
                        <div class="post-content">${post.content}</div>
                        ${post.image_url ? `<img src="${post.image_url}" class="post-image">` : ""}
                        <div class="post-actions">
                            <button class="like-btn" data-id="${post.id}">❤️ ${post.likes_count}</button>
                            <button class="comment-btn" data-id="${post.id}">💬 ${post.comments_count}</button>
                            <button class="collect-btn" data-id="${post.id}">🔖 ${post.collections_count}</button>
                        </div>
                        <div class="comment-section" id="comments-${post.id}" style="display: none;">
                            <div class="comment-list"></div>
                            <textarea class="comment-input" placeholder="Write a comment..." data-id="${post.id}"></textarea>
                            <button class="submit-comment-btn" data-id="${post.id}">Submit</button>
                        </div>
                    `;
                    postList.appendChild(postElement);
                });

                if (!data.has_next) {
                    document.getElementById("loadMoreBtn").style.display = "none";
                }
            })
            .catch(error => console.error("❌ Error loading posts:", error));
    }

    /** ✅ 监听"加载更多"按钮 **/
    document.getElementById("loadMoreBtn").addEventListener("click", function () {
        page += 1;
        loadPosts();
    });

    /** ✅ 监听搜索按钮 **/
    document.getElementById("searchBtn").addEventListener("click", function () {
        searchQuery = document.getElementById("searchInput").value.trim();
        page = 1;
        postList.innerHTML = "";
        loadPosts();
    });

    /** ✅ 监听添加帖子按钮 **/
    document.getElementById("addPostBtn").addEventListener("click", function () {
        modal.show();
    });

    /** ✅ 监听帖子提交 **/
    document.getElementById("postForm").addEventListener("submit", function (event) {
        event.preventDefault();

        let formData = new FormData(this);
        fetch("/discover/posts/create/", {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("✅ Post created successfully!");
                modal.hide();
                location.reload();
            } else {
                alert("❌ " + data.message);
            }
        })
        .catch(error => console.error("❌ Post Error:", error));
    });

    /** ✅ 监听点赞、收藏、评论 **/
    document.addEventListener("click", function (event) {
        let postId = event.target.getAttribute("data-id");

        if (event.target.classList.contains("like-btn")) {
            fetch(`/discover/posts/${postId}/like/`, {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    event.target.innerHTML = `❤️ ${data.likes_count}`;
                } else {
                    alert("❌ " + data.message);
                }
            })
            .catch(error => console.error("❌ Like Error:", error));
        }

        if (event.target.classList.contains("collect-btn")) {
            fetch(`/discover/posts/${postId}/collect/`, {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    event.target.innerHTML = `🔖 ${data.collections_count}`;
                } else {
                    alert("❌ " + data.message);
                }
            })
            .catch(error => console.error("❌ Collect Error:", error));
        }

        if (event.target.classList.contains("comment-btn")) {
            let commentSection = document.getElementById(`comments-${postId}`);

            if (commentSection.style.display === "none") {
                fetch(`/discover/posts/${postId}/comment/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        commentSection.querySelector(".comment-list").innerHTML = "";
                        data.comments.forEach(comment => {
                            let commentElement = document.createElement("div");
                            commentElement.className = "comment";
                            commentElement.innerHTML = `
                                <strong>${comment.author}</strong>: ${comment.content}
                            `;
                            commentSection.querySelector(".comment-list").appendChild(commentElement);
                        });
                        commentSection.style.display = "block";
                    } else {
                        alert("❌ " + data.message);
                    }
                })
                .catch(error => console.error("❌ Comment Error:", error));
            } else {
                commentSection.style.display = "none";
            }
        }

        if (event.target.classList.contains("submit-comment-btn")) {
            let inputField = document.querySelector(`.comment-input[data-id="${postId}"]`);
            let commentText = inputField.value.trim();

            if (!commentText) {
                alert("❌ Comment cannot be empty!");
                return;
            }

            fetch(`/discover/posts/${postId}/comment/`, {
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken(), "Content-Type": "application/x-www-form-urlencoded" },
                body: `content=${encodeURIComponent(commentText)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let commentElement = document.createElement("div");
                    commentElement.className = "comment";
                    commentElement.innerHTML = `<strong>${data.comment.author}</strong>: ${data.comment.content}`;
                    document.getElementById(`comments-${postId}`).querySelector(".comment-list").appendChild(commentElement);
                    inputField.value = "";
                } else {
                    alert("❌ " + data.message);
                }
            })
            .catch(error => console.error("❌ Submit Comment Error:", error));
        }
    });

    loadPosts();
});
