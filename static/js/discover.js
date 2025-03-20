document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ discover.js Loaded");

    let page = 1;
    let searchQuery = "";
    let modal = new bootstrap.Modal(document.getElementById("postModal"));
    let postList = document.getElementById("postList");
    let loadMoreBtn = document.getElementById("loadMoreBtn");
    let searchBtn = document.getElementById("searchBtn");
    let searchInput = document.getElementById("searchInput");

    /** CSRF Token **/
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

    /** Check if the user is logged in **/
    function isUserLoggedIn() {
        return document.body.dataset.userAuthenticated === "true";
    }

    /** Load posts **/
    function loadPosts(isSearch = false) {
        let url = `/discover/posts/?page=${page}&q=${searchQuery}`;
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) {
                    console.error("❌ Failed to load posts:", data.message);
                    return;
                }

                if (isSearch) {
                    postList.innerHTML = "";
                }

                if (data.posts.length === 0 && isSearch) {
                    // Display no results message
                    postList.innerHTML = `
                        <div class="no-results">
                            <p>The content you are looking for is not found.</p>
                            <p>Try searching on Google:</p>
                            <a href="https://www.google.com/search?q=${encodeURIComponent(searchQuery)}" target="_blank" class="google-search-link">
                                Search "${searchQuery}" on Google
                            </a>
                        </div>
                    `;
                    loadMoreBtn.style.display = "none";
                } else {
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
                                <button class="like-btn" data-id="${post.id}" ${!isUserLoggedIn() ? 'disabled' : ''}>❤️ ${post.likes_count}</button>
                                <button class="comment-btn" data-id="${post.id}">💬 ${post.comments_count}</button>
                                <button class="collect-btn" data-id="${post.id}" ${!isUserLoggedIn() ? 'disabled' : ''}>⭐ ${post.collections_count}</button>
                            </div>
                            <div class="comment-section" id="comments-${post.id}" style="display: none;">
                                <div class="comment-list"></div>
                                ${
                                    isUserLoggedIn()
                                        ? `<textarea class="comment-input" placeholder="Write a comment..." data-id="${post.id}"></textarea>
                                        <button class="submit-comment-btn" data-id="${post.id}">Submit</button>`
                                        : `<p class="text-muted">🔒 Log in to comment.</p>`
                                }
                            </div>
                        `;
                        postList.appendChild(postElement);
                    });

                    if (!data.has_next) {
                        loadMoreBtn.style.display = "none";
                    } else {
                        loadMoreBtn.style.display = "block";
                    }
                }

                if (isSearch) {
                    document.getElementById("backBtn").style.display = "block";
                }
            })
            .catch(error => {
                console.error("❌ Error loading posts:", error);
                alert("Failed to load posts. Please try again later.");
            });
    }

    /** Listen for search button click **/
    searchBtn.addEventListener("click", function () {
        searchQuery = searchInput.value.trim();
        if (searchQuery) {
            page = 1; // Reset page number
            loadPosts(true); // Load search results
        }
    });

    /** Listen for back button click **/
    document.getElementById("backBtn").addEventListener("click", function () {
        searchQuery = ""; // Clear search query
        searchInput.value = ""; // Clear search input field
        page = 1; // Reset page number
        loadPosts(); // Reload all posts
        this.style.display = "none"; // Hide back button
    });

    /**  Listen for "Load More" button click **/
    loadMoreBtn.addEventListener("click", function () {
        page += 1;
        loadPosts();
    });

    /**  Listen for "Add Post" button click (redirects to login page for non-logged-in users) **/
    document.getElementById("addPostBtn").addEventListener("click", function () {
        if (!isUserLoggedIn()) {
            window.location.href = "/users/login/"; // Redirect to login page
        } else {
            modal.show();
        }
    });

    /**  Listen for post form submit **/
    document.getElementById("postForm").addEventListener("submit", function (event) {
        event.preventDefault();

        let content = document.getElementById("postContent").value.trim();
        let image = document.getElementById("postImages").files[0];

        if (!content) {
            alert("❌ Content cannot be empty!");
            return;
        }

        let formData = new FormData();
        formData.append("content", content);
        if (image) {
            formData.append("image", image);
        }

        fetch("/discover/posts/create/", {
            method: "POST",
            headers: { "X-CSRFToken": getCSRFToken() },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                modal.hide();
                postList.innerHTML = ""; // Clear current post list
                page = 1; // Reset page number
                loadPosts(); // Reload post list
            } else {
                alert("❌ " + data.message);
            }
        })
        .catch(error => {
            console.error("❌ Create Post Error:", error);
            alert("Failed to create post. Please try again later.");
        });
    });

    /**  Listen for comment button click (toggle comment section) **/
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("comment-btn")) {
            let postId = event.target.getAttribute("data-id");
            let commentSection = document.getElementById(`comments-${postId}`);

            if (commentSection.style.display === "none") {
                fetch(`/discover/posts/${postId}/comment/`, {
                    method: "GET",
                    headers: { "X-CSRFToken": getCSRFToken() }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        let commentList = commentSection.querySelector(".comment-list");
                        commentList.innerHTML = "";

                        data.comments.forEach(comment => {
                            let commentElement = document.createElement("div");
                            commentElement.className = "comment";
                            commentElement.innerHTML = `<strong>${comment.author}</strong>: ${comment.content}`;
                            commentList.appendChild(commentElement);
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
    });

    /**  Listen for submit comment button click (non-logged-in users cannot comment) **/
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("submit-comment-btn")) {
            if (!isUserLoggedIn()) {
                alert("❌ You must be logged in to comment.");
                return;
            }

            let postId = event.target.getAttribute("data-id");
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
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    let commentElement = document.createElement("div");
                    commentElement.className = "comment";
                    commentElement.innerHTML = `<strong>${data.comment.author}</strong>: ${data.comment.content}`;
                    document.getElementById(`comments-${postId}`).querySelector(".comment-list").appendChild(commentElement);
                    inputField.value = "";

                    // Update comment count
                    let commentBtn = document.querySelector(`.comment-btn[data-id="${postId}"]`);
                    commentBtn.innerHTML = `💬 ${data.comments_count}`;
                } else {
                    alert("❌ " + data.message);
                }
            })
            .catch(error => console.error("❌ Submit Comment Error:", error));
        }
    });

    /**  Listen for like & collect button click **/
    document.addEventListener("click", function (event) {
        if (!isUserLoggedIn()) {
            alert("❌ You must be logged in to like, collect, search posts and post comment.");
            return;
        }

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
    });

    /**  Initialize loading posts **/
    loadPosts();
});
