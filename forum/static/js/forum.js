var selectedBookId;
var userIdElement = document.getElementById("user-id");
var userId = userIdElement.textContent;
var path = window.location.pathname;

async function getPosts() {
  return fetch("/forum/get-post/").then((res) => res.json());
}
async function getCommentsByPostId(post_id) {
  return fetch(`/forum/get-comments/${post_id}/`).then((res) => res.json());
}
async function getUserById(user_id) {
  return fetch(`/forum/get-user/${user_id}/`).then((res) => res.json());
}
async function getBooks() {
  return fetch("/api/books").then((res) => res.json());
}
async function getPostById(post_id) {
  return fetch(`/forum/get-post/${post_id}/`).then((res) => res.json());
}
async function getBookById(book_id) {
  return fetch(`/api/books/${book_id}`).then((res) => res.json());
}
async function getCategories() {
  return fetch("/api/categories").then((res) => res.json());
}
async function listBooks() {
  const books = await getBooks();
  let htmlStrings = [];
  for (const book of books) {
    let htmlString = `<h4 id="${book.id}"><a class="dropdown-item book-item">${book.title}</a></h4>`;
    htmlStrings.push(htmlString);
  }
  document.getElementById("book-list").innerHTML += htmlStrings.join("");

  var input = document.querySelector("#form1");
  input.addEventListener("keyup", function () {
    var value = this.value.toLowerCase();
    var items = document.querySelectorAll("#book-list h4");
    items.forEach(function (item) {
      if (item.textContent.toLowerCase().indexOf(value) > -1) {
        item.style.display = "";
      } else {
        item.style.display = "none";
      }
    });
  });

  var bookItems = document.querySelectorAll(".book-item");
  bookItems.forEach(function (item) {
    item.addEventListener("click", function () {
      selectedBookId = this.parentElement.id;
      input.value = this.textContent;
    });
  });
}

document
  .querySelector("#add-buku")
  .addEventListener("click", async function () {
    if (!selectedBookId) return;

    const response = await fetch(`/api/books/${selectedBookId}/`, {
      method: "GET",
    });
    const book = await response.json();
    document.getElementById("book-selected").value = selectedBookId;
    document.getElementById(
      "upload-status-book"
    ).innerHTML = `<div class="card p-1 rounded-5">
          <div class="card-body d-flex p-1 align-items-center">
            <h6 id="book-title" class="mb-0 fs-6">Book: ${book.title}</h6>   
            <a id="cancel-upload-book" class="mb-1"><i class="bi bi-x"></i></a>    
          </div>
        </div>
`;

    document
      .querySelector("#cancel-upload-book")
      .addEventListener("click", function () {
        document.getElementById("book-selected").value = "";
        document.getElementById("upload-status-book").innerHTML = "";
      });
  });

async function listCategories() {
  const categories = await getCategories();
  const htmlStrings = [];
  for (const categori of categories) {
    const htmlString = `
      <hr class="m-0"/>
      <li class="px-2 pt-1"><h4 id="category" onclick="changeUrlAndRefreshPosts('${categori.name}')">${categori.name}</h4></li>
      `;
    htmlStrings.push(htmlString);
  }
  document.getElementById("categories-list").innerHTML += htmlStrings.join("");
  var input = document.querySelector("#my-input");
  input.addEventListener("keyup", function () {
    var value = this.value.toLowerCase();
    var items = document.querySelectorAll(".dropdown-menu li");
    items.forEach(function (item) {
      if (item.textContent.toLowerCase().indexOf(value) > -1) {
        item.style.display = "";
      } else {
        item.style.display = "none";
      }
    });
  });
}

function changeUrlAndRefreshPosts(name) {
  let params = new URLSearchParams();

  params.append("category", name);

  history.pushState(null, "", `/forum/?${params.toString()}`);

  addCategoryToPage(name);

  refreshPosts();
}

function addCategoryToPage(name) {
  document.getElementById(
    "category-selected"
  ).innerHTML = `<div class="card px-1 rounded-5">
          <div class="card-body d-flex p-1 justify-content-center align-items-center">
            <h4 id="category-name" class="mb-0 fs-6 text-center">${name}</h4>   
            <a id="cancel-select" class="text-center"><i class="bi bi-x"></i></a>    
          </div>
        </div>
`;
  document
    .getElementById("cancel-select")
    .addEventListener("click", function () {
      document.getElementById("category-selected").innerHTML = "";
      history.pushState(null, "", "/forum/");
      localStorage.removeItem("selectedCategory");
      refreshPosts();
    });
}

listBooks();
listCategories();

async function refreshPosts() {
  let posts = await getPosts();
  const user_id = userId;
  let params = new URLSearchParams(document.location.search);
  let category = params.get("category");
  if (category) {
    addCategoryToPage(category);
    posts = await posts.reduce(async (accPromise, post) => {
      const acc = await accPromise;
      if (post.fields.book) {
        const book = await getBookById(post.fields.book);
        if (book.categories[0].name === category) {
          acc.push(post);
        }
      }
      return acc;
    }, Promise.resolve([]));
  }

  posts.sort(
    (a, b) => new Date(b.fields.date_added) - new Date(a.fields.date_added)
  );
  const htmlStrings = [];
  for (const post of posts) {
    let comments = await getCommentsByPostId(post.pk);
    let numComments = comments.length;
    let book = null;
    if (post.fields.book) {
      book = await getBookById(post.fields.book);
    }
    let user = await getUserById(post.fields.user);
    let dateAdded = new Date(post.fields.date_added);
    let now = new Date();
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
    let htmlString = `
      <article class="card mb-3 shadow bg-light w-sm-full" onclick="window.location.href='post/${post.pk}'">
          <div class="card-body">
              <div class="d-flex justify-content-between m-0">
                  <h4 id="username" class="text-dark m-0 fw-bold">${user[0].fields.username} <span id="time-dif" class="fw-normal fs-6"> · ${timeDifference}</span></h4>`;
    if (post.fields.user == user_id) {
      htmlString += `<div class="btn-group">
        <button id="t-dot" class="btn btn-sm border-0 top-0 m-0" type="button" data-bs-toggle="dropdown" aria-expanded="false" onclick="event.stopPropagation();"">
          <i class="bi bi-three-dots"></i>
        </button>
        <ul id="option" class="dropdown-menu rounded p-0 my-0 shadow bg-light">
          <li class="px-0 mx-0 fs-6">
            <h4 type="button" class="btn text-dark border-0 fs-6 w-100 m-0 text-start" data-bs-toggle="modal" data-bs-target="#deleteModal" onclick="clickDelete(event,${post.pk});"><i class="bi bi-trash-fill text-dark"></i> Delete</h4>  
          </li>
          <li class="p-0 m-0 fs-6">
            <h4 type="button" class="btn text-dark border-0 fs-6 w-100 m-0 text-start" data-bs-toggle="modal" data-bs-target="#editModal" onclick="clickEdit(event,${post.pk});"><i class="bi bi-pencil-fill text-dark"></i> Edit</h4>    
          </li>
        </ul>
      </div>
      `;
    }
    htmlString += `</div>
              <h2 id="post-title" class="card-title m-0">${post.fields.title}</h2>
              <h4 id="post-text" class="card-text">${post.fields.text}</h4>`;
    if (post.fields.book) {
      htmlString += `<div class="card w-sm-auto">
                <div class="card-body">
                  <h5 class="card-title">${book.title}</h5>
                  <h6 class="card-subtitle mb-2 text-muted">${book.authors[0].name}</h6>
                  <h6 class="card-subtitle mb-2 text-muted">${book.categories[0].name}</h6>
                </div>
              </div>
              `;
    }
    htmlString += `<div id="com-count" class="mt-1 fw-normal fs-6"> <i id="com-icon" class="bi bi-chat"></i> ${numComments}</div>
          </div>
      </article>
  `;
    htmlStrings.push(htmlString);
  }

  document.getElementById("posts").innerHTML = htmlStrings.join("");
}
refreshPosts();

function addPost() {
  fetch("/forum/create-post/", {
    method: "POST",
    body: new FormData(document.querySelector("#form-post")),
  }).then(refreshPosts);
  document.getElementById("form-post").reset();
  document.querySelector("#form1").value = "";
  document.getElementById("book-selected").value = "";
  document.getElementById("upload-status-book").innerHTML = "";
  return false;
}

function editPost(post_id) {
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  const headers = new Headers({
    "X-CSRFToken": csrfToken,
  });
  fetch(`edit-post/${post_id}/`, {
    method: "POST",
    body: new FormData(document.querySelector("#form-post-edit")),
    headers: headers,
  }).then(refreshPosts);

  document.getElementById("form-post-edit").reset();
  return false;
}

document.getElementById("button_add").addEventListener("click", function () {
  document.getElementById("upload-status-book").innerHTML = "";
});

function clickDelete(event, post_id) {
  event.stopPropagation();
  document.getElementById("btn-delete").addEventListener("click", function (e) {
    deletePost(post_id);
  });
}

async function clickEdit(event, post_id) {
  event.stopPropagation();
  const response = await getPostById(post_id);
  console.log(response[0].fields.title);
  document.getElementById("title-edit").value = response[0].fields.title;
  document.getElementById("description-edit").innerHTML =
    response[0].fields.text;
  document.getElementById("book-selected-edit").value = response[0].fields.book;
  var btnEdit = document.getElementById("btn-edit");
  var newBtnEdit = btnEdit.cloneNode(true);
  btnEdit.parentNode.replaceChild(newBtnEdit, btnEdit);
  newBtnEdit.addEventListener("click", function (e) {
    editPost(post_id);
  });
}
function deletePost(post_id) {
  fetch(`delete-post/${post_id}/`, {
    method: "DELETE",
  }).then(refreshPosts);
  var modalElement = document.getElementById("deleteModal" + post_id);
  var modalInstance = bootstrap.Modal.getInstance(modalElement);
  modalInstance.hide();
  return false;
}

document.getElementById("button_add").addEventListener("click", function () {
  document.getElementById("form1").value = "";
});

document.getElementById("button_add").onclick = addPost;
