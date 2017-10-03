import axios from 'axios';

export const listComments = (comments) => ({
	type: "LIST_COMMENTS",
	comments,
});

export const addComment = (comment) => ({
	type: "ADD_COMMENT",
	comment
});

export const fetchComments = (postId, token) => (
  function(dispatch){
    axios({
      method: 'get',
      url: 'http://localhost:8000/testapp/comment/'+postId+'/',
      headers: {
      Authorization: 'Token '+token,
      }
    })
    .then(response => {
        dispatch(listComments(response.data))

    })
    .catch(function(error){
        alert("Something Went Wrong")
    })
	}
)

export const addCommentApi = (comment, postId, token) => (
  function(dispatch){
    let data = new FormData()
    data.set('comment', comment.value)

    axios({
        method: 'post',
        url: 'http://localhost:8000/testapp/comment/'+postId+'/',
        headers: {
        Authorization: 'Token '+ token,
        },
        data: data
    })
    .then(response => {
        dispatch(addComment(response.data))

    })
    .catch(function(error){
        alert("Something Went Wrong")
    })      
  }
)