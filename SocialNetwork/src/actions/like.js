import axios from 'axios';
import {postLiked} from './post'


export const listLikes = (likes) => ({
	type: "LIST_LIKES",
	likes,
});

export const addLike = (like) => ({
	type: "ADD_LIKE",
	like
});

export const fetchLikes = (postId, token) => (
	function(dispatch){
		axios({
      method: 'get',
      url: 'http://localhost:8000/testapp/like/'+postId+'/',
      headers: {
      Authorization: 'Token '+token,
      }
    })
    .then(response => {
        dispatch(listLikes(response.data))

    })
    .catch(function(error){
          alert("Something Went Wrong")
    })
	}
)

export const addLikeApi = (postId, token) => (
	function(dispatch){
		axios({
      method: 'post',
      url: 'http://localhost:8000/testapp/like/'+postId+'/',
      headers: {
      Authorization: 'Token '+ token,
        },
    })
    .then(response => {
      dispatch(addLike(response.data))
      dispatch(postLiked(postId))
    })
    .catch(function(error){
      alert("Something Went Wrong")
    })
	}
)