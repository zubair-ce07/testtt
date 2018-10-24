function makeAjaxCall(callType, callUrl, callData)
{
  return $.ajax({
    type        : callType,
    url         : callUrl,
    data        : callData,
    dataType    : `json`
  })

}


function getUserList(username) {
  return fetch(`${BASEURL}/users?username=${username}`)
    .then(response => response.json())
}


function getAllPosts() {
  return fetch(`${BASEURL}/posts`)
    .then(response => response.json())
    .catch(console.error);
}


function getUrlsData(urls)
{
  return Promise.all(urls.map(url => fetch(url)))
    .then(responses => Promise.all(responses.map(res => res.json())))
    .catch(console.error);
}


function getPostCommentsAndUser(post)
{
  let urls = [
    `${BASEURL}/posts/${post.id}/comments`,
    `${BASEURL}/users/${post.userId}`
  ];
  
  return getUrlsData(urls)
    .then(data =>
    {
      post.postComments = data[0];
      post.postUser = data[1];
      return post
    })
}
