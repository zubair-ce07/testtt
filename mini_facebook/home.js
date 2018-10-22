/**
 * [logoutUser - call when user clik on logout button]
 * reason: needed to clear local storge and for redirection to index page
 */
function logoutUser()
{
  localStorage.removeItem(`loggedin_user`);
  window.location.href = `index.html`;
}


/**
 * [getCurrentDate - return current date in specific format]
 * reason: we need to store curret date string as a posted-date
 * @return {string} [current date string]
 */
function getCurrentDate()
{
  let date = new Date();
  let month = MONTHS[date.getMonth()-1];
  return `${month} ${date.getDate()}, ${date.getFullYear()}`;
}


/**
 * [increaseCommentBadge - increase comment count on badge of specific post]
 * reason: After adding comment we need to increase comment count on badge.
 * @param  {int} postId [id of the post of which badge need to be incremented] 
 */
function increaseCommentBadge(postId)
{
  let commentBadge = document.getElementById(`${postId}_commentBadge`);
  let count = commentBadge.innerHTML;
  count= parseInt(count, 10)+1;
  commentBadge.innerHTML = count;
}


/**
 * [getPostDiv - return new empty post div after cloning post template]
 * reason: needed to append and display new post in a container
 * @return {string} [new cloned div]
 */
function getPostDiv()
{
  let postTemplate = document.getElementsByName(`post_template`)[0];
  let post = postTemplate.content.querySelector(`.post`);
  let postDiv = document.importNode(post, true);
  return postDiv;
}


/**
 * [handleLikes - handle likes array if it is pointing to string element or there is no like array]
 * reason: needed in cases when likeArray (likes[]) is not there in a response object (for newly created post) or
 *         if there is only element in array then array is pointing directly to that element (likes[] = "usernamme")
 * @param  {array} likes [current likes array that can be undefine or a single element (array of char) or array of usrenames] 
 * @return {array} [likes array that contain usernames]
 */
function handleLikes(likes)
{
  /*
    if likes array is not there => form new arrray 
    if there is single element (likes array is pointing directly to that element)  
      => form new array and push that only element
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


/**
 * [displayComment - display comment in a new cloned comment div
 *   + append that comment div in a comments container
 * ]
 * reason: needed to display comments of every post from database list or after adding a new comment
 * @param  {string} commentContainer [comment conatainer of a specific post]
 * @param  {string} comment [comment that needed to be displayed]
 */
function displayComment(commentContainer, comment)
{
  let commentDiv = commentContainer.firstElementChild.cloneNode(true);
  commentDiv.getElementsByClassName(`comment-by`)[0].innerHTML = comment[`comment_by`];
  commentDiv.getElementsByClassName(`comment`)[0].innerHTML = comment[`comment`];
  commentContainer.appendChild(commentDiv);
}


/**
 * [displayPost - display post in a given post div]
 * reason: needed to display all posts from database list or after adding a new post
 * @param  {object} userPost [post that need to be display]
 * @param  {string} postDiv [div in which post is needed to be displayed]
 */
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


/**
 * [makePost - make new post through API call and append that post in a post container]
 * reason: calls when user wanted to make a new post
 */
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
      url         : `${BASEURL}/users/${loggedInUser.id}/posts`,
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
        document.getElementById(`newPostTitle`).value = '';
        document.getElementById(`newPostText`).value = '';
      });
  }
}


/**
 * [makeComment - make new comment through API call 
 *   + display that comment in a  comment container of specific post
 *   + increase badge comment count
 * ]
 * reason: calls when user wanted to make a new comment
 */
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
    url         : `${BASEURL}/posts/${postId}/comments`,
    data        : formData,
    dataType    : `json`
  })
    .done(comment =>
    {
      let commentContainer = document.getElementById(`${comment.postId}_comments`);
      displayComment(commentContainer, comment);
      increaseCommentBadge(comment.postId);
      document.getElementById(`${postId}_comment`).value = '';
    });
}


/**
 * [makeLike - add or remove username from a like array through API call
 *   + toggle like button
 *   + update like count badge 
 * ]
 * reason: calls when user like or unlike a post
 */
function makeLike()
{
  let loggedInUser = JSON.parse(localStorage.getItem(`loggedin_user`));
  event.srcElement.classList.toggle(`fa-thumbs-down`);
  let postId = (event.srcElement.id.split(`_`))[0];

  fetch(`${BASEURL}/posts/${postId}`)
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
        url         : `${BASEURL}/posts/${postId}`,
        data        : post,
        dataType    : `json`
      })
        .done(() => document.getElementById(`${postId}_likecount`).innerHTML = post[`likes[]`].length);
    })
    .catch(console.error);
}


/**
 * [addClickEvent - add click event to a specific object]
 * @param  {object} className [class-name of the object on which listener is needed to be attached]
 * @param  {function} functionName [call back function for the event]
 * reason: calls in start
 */
function addClickEvent(className, functionName)
{
  let btnArr = document.getElementsByClassName(className);
  Array.from(btnArr).forEach(element => element.addEventListener(`click`, functionName));
}


/**
 * [getPostUser - get user (owner) of the post ]
 * @param  {object} userPost [post object]
 * reason: needed to display username on posts
 */
function getPostUser(userPost)
{
  if(loggedInUser.id == userPost.userId)
  {  
    userPost[`post_user`] = loggedInUser;
  }
  else
  {
    fetch(`${BASEURL}/users/${userPost.userId}`)
      .then(response => response.json())
      .then(postUser => userPost[`post_user`] = postUser)
      .catch(console.error);
  }
}


/**
 * [ loadAllPosts - append all posts after getting post-list through API call in a post container ]
 * reason: needed to display all posts
 */
function loadAllPosts()
{
  let loggedInUser = JSON.parse(localStorage.getItem(`loggedin_user`));
  fetch(`${BASEURL}/posts`)
    .then(response => response.json())
    .then(postList =>
    {
      let postContainer = document.getElementById(`postContainer`);
      for (let userPost of postList)
      {
        fetch(`${BASEURL}/posts/${userPost.id}/comments`)
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
}


addClickEvent(`logout-btn`, logoutUser);
loadAllPosts()
