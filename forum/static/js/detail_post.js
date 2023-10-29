var userIdElement = document.getElementById("user-id");
var userId = userIdElement.textContent;
var postIdElement = document.getElementById("post-id");
var postId = postIdElement.textContent;

async function getCommentsByPostId(post_id) {
  return fetch(`/forum/get-comments/${post_id}/`).then((res) => res.json());
}
async function getCommentById(comment_id) {
  return fetch(`/forum/get-comment/${comment_id}/`).then((res) => res.json());
}
async function getUserById(user_id) {
  return fetch(`/forum/get-user/${user_id}/`).then((res) => res.json());
}
async function getPostById(post_id) {
  return fetch(`/forum/get-post/${post_id}/`).then((res) => res.json());
}
async function getBookById(book_id) {
  return fetch(`/api/books/${book_id}`).then((res) => res.json());
}
function calculateTime(now, dateAdded) {
  let diffInMilliseconds = now - dateAdded;
  let diffInSeconds = diffInMilliseconds / 1000;
  let diffInMinutes = diffInSeconds / 60;
  let diffInHours = diffInMinutes / 60;
  let diffInDays = diffInHours / 24;

  let timeDifference;
  if (diffInSeconds < 60) {
    timeDifference = Math.round(diffInSeconds) + " s";
  } else if (diffInMinutes < 60) {
    timeDifference = Math.round(diffInMinutes) + " m";
  } else if (diffInHours < 24) {
    timeDifference = Math.round(diffInHours) + " h";
  } else {
    timeDifference = Math.round(diffInDays) + " d";
  }
  return timeDifference;
}

function addPost() {
  fetch("/forum/create-post/", {
    method: "POST",
    body: new FormData(document.querySelector("#form-post")),
  }).then(refreshPosts);

  document.getElementById("form-post").reset();
  document.getElementById("image").value = "";
  document.getElementById("upload-image").innerHTML = "";
  document.getElementById("book").value = "";
  document.getElementById("upload-status-book").innerHTML = "";
  return false;
}

function addComment() {
  fetch(`/forum/create-comment/${postId}/`, {
    method: "POST",
    body: new FormData(document.querySelector("#form-comment")),
  }).then(refreshPosts);

  document.getElementById("form-comment").reset();
  return false;
}
var authenticatedElement = document.getElementById("authenticated");
var authenticatedText = authenticatedElement.textContent;
if (authenticatedText === "True") {
  document.getElementById("button_add_comment").onclick = addComment;
}

async function refreshPosts() {
  const user_id = userId;
  const post_id = postId;
  const post = await getPostById(post_id);
  let book = null;
  if (post[0].fields.book) {
    book = await getBookById(post[0].fields.book);
  }
  const htmlStrings = [];
  const comments = await getCommentsByPostId(post[0].pk);
  console.log(comments);
  let user = await getUserById(post[0].fields.user);
  let dateAdded = new Date(post[0].fields.date_added); // asumsikan ini adalah tanggal saat post ditambahkan
  let now = new Date(); // waktu saat ini

  let timeDifference = calculateTime(now, dateAdded);
  let htmlString = `
                    <div class="card mb-3 shadow-sm bg-light">
                      <div class="card-body">
                          <div class="d-flex justify-content-between">
                                <h4 class="text-dark fw-bold">${user[0].fields.username} <span class="fw-normal fs-6"> · ${timeDifference}</span></h4>`;
  if (post[0].fields.user == user_id) {
    htmlString += `<div class="btn-group">
          <button class="btn btn-sm border-0 top-0 m-0" type="button" data-bs-toggle="dropdown" aria-expanded="false" onclick="event.stopPropagation();"">
            <i class="bi bi-three-dots"></i>
          </button>
          <ul class="dropdown-menu rounded p-0 my-0 shadow bg-light">
            <li class="px-0 mx-0 fs-6">
              <h4 type="button" class="btn text-dark border-0 fs-6 w-100 m-0 text-start" data-bs-toggle="modal" data-bs-target="#deleteModalPost" onclick="clickDelete(event,${post[0].pk}, true);"><i class="bi bi-trash-fill text-dark"></i> Delete</h4>  
            </li>
            <li class="p-0 m-0 fs-6">
              <h4 type="button" class="btn text-dark border-0 fs-6 w-100 m-0 text-start" data-bs-toggle="modal" data-bs-target="#editModalPost" onclick="clickEdit(event,${post[0].pk}, true);"><i class="bi bi-pencil-fill text-dark"></i> Edit</h4>    
            </li>
          </ul>
        </div>`;
  }
  htmlString += `</div>
              <h2 id="post-title" class="card-title m-0">${post[0].fields.title}</h2>
                <h4 id="post-text" class="card-text">${post[0].fields.text}</h4>`;
  if (post[0].fields.book) {
    htmlString += `<div class="card" id="book-post">
                  <div class="card-body">
                    <h5 class="card-title">${book.title}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">${book.authors[0].name}</h6>
                    <h6 class="card-subtitle mb-2 text-muted">${book.categories[0].name}</h6>
                  </div>
                </div>
                `;
  }
  if (post[0].fields.image) {
    htmlString += `<img src="/media/${post[0].fields.image}" class="card-img-top w-50 h-50 img-fluid rounded" alt="${post[0].fields.title}">`;
  }
  htmlStrings.push(htmlString);
  document.getElementById("posts").innerHTML = htmlStrings.join("");
  htmlString = "";
  if (comments) {
    comments.sort(
      (a, b) => new Date(b.fields.date_added) - new Date(a.fields.date_added)
    );
    for (const comment of comments) {
      let dateAdded = new Date(comment.fields.date_added); // asumsikan ini adalah tanggal saat post ditambahkan
      let now = new Date(); // waktu saat ini
      timeDifference = calculateTime(now, dateAdded);
      htmlString += `
                      <div class="card mt-3 ml-5 bg-light shadow">
                        <div class="card-body">
                          <div class="d-flex justify-content-between">
                            <h4 class="text-dark fw-bold">${user[0].fields.username} <span class="fw-normal fs-6"> · ${timeDifference}</span></h4>`;
      if (comment.fields.user == user_id) {
        htmlString += ` 
          <div class="btn-group">
          <button class="btn btn-sm border-0 top-0 m-0" type="button" data-bs-toggle="dropdown" aria-expanded="false" onclick="event.stopPropagation();"">
            <i class="bi bi-three-dots"></i>
          </button>
          <ul class="dropdown-menu rounded p-0 my-0 shadow bg-light">
            <li class="px-0 mx-0 fs-6">
              <h4 type="button" class="btn text-dark border-0 fs-6 w-100 m-0 text-start" data-bs-toggle="modal" data-bs-target="#deleteModalComment" onclick="clickDelete(event,${comment.pk}, false);"><i class="bi bi-trash-fill text-dark"></i> Delete</h4>  
            </li>
            <li class="p-0 m-0 fs-6">
              <h4 type="button" class="btn text-dark border-0 fs-6 w-100 m-0 text-start" data-bs-toggle="modal" data-bs-target="#editModalComment" onclick="clickEdit(event,${comment.pk}, false);"><i class="bi bi-pencil-fill text-dark"></i> Edit</h4>    
            </li>
          </ul>
        </div>`;
      }
      htmlString += `
      </div><p class="card-text">${comment.fields.text}</p></div></div>`;
    }
  }
  document.getElementById("comments").innerHTML = htmlString;
}

refreshPosts();

function editPost() {
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;

  // Construct the headers including the CSRF token
  const headers = new Headers({
    "X-CSRFToken": csrfToken, // Include the CSRF token here
  });
  fetch(`/forum/edit-post/${postId}/`, {
    method: "POST",
    body: new FormData(document.querySelector("#form-post-edit")),
    headers: headers,
  }).then(refreshPosts);

  document.getElementById("form-post-edit").reset();
  return false;
}

function clickDelete(event, post_id, isPost) {
  event.stopPropagation();
  if (isPost) {
    document
      .getElementById("btn-delete")
      .addEventListener("click", function (e) {
        deletePost(post_id);
      });
  } else {
    document
      .getElementById("btn-delete-comment")
      .addEventListener("click", function (e) {
        deleteComment(post_id);
      });
  }
}

async function clickEdit(event, id, isPost) {
  event.stopPropagation();
  if (isPost) {
    const response = await getPostById(id);
    document.getElementById("title-edit").value = response[0].fields.title;
    document.getElementById("description-edit").innerHTML =
      response[0].fields.text;
    document.getElementById("book-selected-edit").value =
      response[0].fields.book;
    document.getElementById("btn-edit").addEventListener("click", function (e) {
      editPost();
    });
  } else {
    const response = await getCommentById(id);
    document.getElementById("content-edit").innerHTML = response[0].fields.text;
    var btnEdit = document.getElementById("btn-edit-comment");
    var newBtnEdit = btnEdit.cloneNode(true);
    btnEdit.parentNode.replaceChild(newBtnEdit, btnEdit);
    newBtnEdit.addEventListener("click", function (e) {
      editComment(id);
    });
  }
}

function editComment(post_id) {
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;

  // Construct the headers including the CSRF token
  const headers = new Headers({
    "X-CSRFToken": csrfToken, // Include the CSRF token here
  });
  fetch(`/forum/edit-comment/${post_id}/`, {
    method: "POST",
    body: new FormData(document.querySelector("#form-comment-edit")),
    headers: headers,
  }).then(refreshPosts);

  document.getElementById("form-comment-edit").reset();
  return false;
}
function deletePost(post_id) {
  fetch(`/forum/delete-post/${post_id}/`, {
    method: "DELETE",
  })
    .then(() => (window.location.href = "/forum"))
    .then(refreshPosts);
  return false;
}

function deleteComment(comment) {
  fetch(`/forum/delete-comment/${comment}/`, {
    method: "DELETE",
  }).then(refreshPosts);
  return false;
}
