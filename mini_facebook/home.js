function logoutUser()
{
  localStorage.removeItem(`loggedin_user`);
  window.location.href = `index.html`;
}


function getCurrentDate()
{
  let date = new Date();
  let month = months[date.getMonth()-1];
  return `${month} ${date.getDate()}, ${date.getFullYear()}`;
}


function increaseCommentBadge(postId)
{
  let commentBadge = document.getElementById(`${postId}_commentBadge`);
  let count = commentBadge.innerHTML;
  count= parseInt(count, 10)+1;
  commentBadge.innerHTML = count;
}


function getPostDiv()
{
  let postTemplate = document.getElementsByName(`post_template`)[0];
  let post = postTemplate.content.querySelector(`.post`);
  let postDiv = document.importNode(post, true);
  return postDiv;
}

function handleLikes(likes)
{
  /*
    if likes array is not there => form new arrray 
    if there is single element (likes array is pointing directly to that element)  
      => form new array with that element
  */
  if(!likes)
  {
    return new Array();
  }
  else if (!Array.isArray(likes))
  {
    return (new Array()).push(likes);
  }
  else
    return likes;
}


function displayComment(commentContainer, comment)
{
  let commentDiv = commentContainer.firstElementChild.cloneNode(true);
  commentDiv.getElementsByClassName(`comment-by`)[0].innerHTML = comment[`comment_by`];
  commentDiv.getElementsByClassName(`comment`)[0].innerHTML = comment[`comment`];
  commentContainer.appendChild(commentDiv);
}

function displayPost(userPost, postDiv)
{
  let loggedInUser = JSON.parse(localStorage.getItem(`loggedin_user`));
  userPost[`likes[]`] =  handleLikes(userPost[`likes[]`]);

  postDiv.getElementsByClassName(`post-username`)[0].innerHTML = userPost[`post_user`][`username`];
  postDiv.getElementsByClassName(`post-date`)[0].innerHTML = userPost.date;
  postDiv.getElementsByClassName(`post-title`)[0].innerHTML = userPost.title;
  postDiv.getElementsByClassName(`post-data`)[0].innerHTML = userPost.post;

  let commentBadge = postDiv.getElementsByClassName(`post-comment-count`)[0];
  commentBadge.innerHTML =  userPost[`post_comments`].length;
  commentBadge.id = `${userPost.id}_commentBadge`;

  let likeBadge = postDiv.getElementsByClassName(`post-likes`)[0];
  likeBadge.innerHTML = userPost[`likes[]`].length;
  likeBadge.id = `${userPost.id}_likecount`;

  let likeElement = postDiv.getElementsByClassName(`like`)[0];
  likeElement.id =  `${userPost.id}_like`;

  if(userPost[`likes[]`].includes(loggedInUser.username))
  {
    likeElement.classList.add(`fa-thumbs-down`);
  }
  else
  {
    likeElement.classList.add(`fa-thumbs-up`);
  }

  postDiv.getElementsByClassName(`comment-btn`)[0].id =  `${userPost.id}_btn`;
  postDiv.getElementsByClassName(`comment-area`)[0].id =  `${userPost.id}_comment`;

  let commentContainer = postDiv.getElementsByClassName(`comment-container`)[0];
  commentContainer.id = `${userPost.id}_comments`;

  for(let comment of userPost[`post_comments`])
  {
    displayComment(commentContainer, comment);
  }
}


function makePost()
{
  let loggedInUser = JSON.parse(localStorage.getItem(`loggedin_user`));
  if(loggedInUser)
  {
    let formData = 
    {
      "title": document.getElementById(`newPostTitle`).value,
      "post": document.getElementById(`newPostText`).value,
      "date": getCurrentDate()
    };

    $.ajax({
      type        : `POST`,
      url         : `${baseUrl}/users/${loggedInUser.id}/posts`,
      data        : formData,
      dataType    : `json`
    })
      .done(newPost =>
      {
        let postContainer = document.getElementById(`postContainer`);
        let postDiv = getPostDiv();
        newPost[`post_comments`] = [];
        newPost[`post_user`] = loggedInUser;
        displayPost(newPost, postDiv);
        postContainer.appendChild(postDiv);
        document.getElementById(`addMsg`).innerHTML = `your post has been posted...`;
        document.getElementById(`newPostTitle`).value = ``;
        document.getElementById(`newPostText`).value = ``;
      });
  }
}


function makeComment()
{
  let postId = (event.srcElement.id.split(`_`))[0];
  let loggedInUser = JSON.parse(localStorage.getItem(`loggedin_user`));

  let formData = {
    "comment_by": loggedInUser.username,
    "comment": document.getElementById(`${postId}_comment`).value
  };

  $.ajax({
    type        : `POST`,
    url         : `${baseUrl}/posts/${postId}/comments`,
    data        : formData,
    dataType    : `json`
  })
    .done(comment =>
    {
      let commentContainer = document.getElementById(`${comment.postId}_comments`);
      displayComment(commentContainer, comment);
      increaseCommentBadge(comment.postId);
      document.getElementById(`${postId}_comment`).value = ``;
    });
}


function makeLike()
{
  let loggedInUser = JSON.parse(localStorage.getItem(`loggedin_user`));
  event.srcElement.classList.toggle(`fa-thumbs-down`);
  let postId = (event.srcElement.id.split(`_`))[0];

  fetch(`${baseUrl}/posts/${postId}`)
    .then(response => response.json())
    .then(post =>
    {
      post[`likes[]`] =  handleLikes(post[`likes[]`]);
      let likeIndex = post[`likes[]`].findIndex(username => username == loggedInUser.username);
      if(likeIndex!=-1)
      {
        post[`likes[]`].splice(likeIndex, 1);
      }
      else
        post[`likes[]`].push(loggedInUser.username);

      $.ajax({
        type        : `PUT`,
        url         : `${baseUrl}/posts/${postId}`,
        data        : post,
        dataType    : `json`
      })
        .done(() => document.getElementById(`${postId}_likecount`).innerHTML = post[`likes[]`].length);
    })
    .catch(console.error);
}


function addClickEvent(className, functionName)
{
  let btnArr = document.getElementsByClassName(className);
  Array.from(btnArr).forEach(element => element.addEventListener(`click`, functionName));
}


function getPostUser(userPost)
{
  if(loggedInUser.id == userPost.userId)
  {  
    userPost[`post_user`] = loggedInUser;
  }
  else
  {
    fetch(`${baseUrl}/users/${userPost.userId}`)
      .then(response => response.json())
      .then(postUser => userPost[`post_user`] = postUser)
      .catch(console.error);
  }
}

addClickEvent(`logout-btn`, logoutUser);
let loggedInUser = JSON.parse(localStorage.getItem(`loggedin_user`));
fetch(`${baseUrl}/posts`)
  .then(response => response.json())
  .then(postList =>
  {
    let postContainer = document.getElementById(`postContainer`);
    for (let userPost of postList)
    {
      fetch(`${baseUrl}/posts/${userPost.id}/comments`)
        .then(response => response.json())
        .then(postComments =>
        {
          userPost[`post_comments`] = postComments;
          getPostUser(userPost);
          let postDiv = getPostDiv();
          displayPost(userPost, postDiv);
          postContainer.appendChild(postDiv);
        }).catch(console.error);
    }
  }).catch(console.error);
