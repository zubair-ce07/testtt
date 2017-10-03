import axios from 'axios'
import { LIST_POSTS, ADD_POST, POST_LIKED, PRIVACY_CHANGED} from './actions'


export const listPost = (posts,posts_count,likes_count) => ({
	type: LIST_POSTS,
	posts,
	posts_count,
	likes_count,
});

export const addPost = (post) => ({
	type: ADD_POST,
	post
});

export const postLiked = (id) => ({
	type: POST_LIKED,
	postId: id
});

export const privacyChanged = (id, privacy) => ({
	type: PRIVACY_CHANGED,
	postId: id,
	privacy
});

export const addPostApi = (caption, file, token, privacy, fileType) => (
  function(dispatch){
		let data = new FormData()

		data.set('file', file.files[0])
		data.set('caption', caption.value)
		data.set('file_type', fileType)
		data.set('privacy', privacy)

		axios({
      method: 'post',
      url: 'http://localhost:8000/testapp/post',
      headers: {
      Authorization: 'Token ' + token,
      },
      data: data
    })
    .then(response => {
      dispatch(addPost(response.data.post))
    })
    .catch(function(error){
      alert("Post not created.")
    })
	}
)

export const fetchPosts = (token) => (
  function(dispatch){
    axios({
      method: 'get',
      url: 'http://localhost:8000/testapp/post',
      headers: {
      Authorization: 'Token '+token,
      }
    })
    .then(response => {
      const {posts, posts_count, likes_count} = response.data
      dispatch(listPost(posts, posts_count, likes_count))
    })
    .catch(function(error){
      alert("Something Went Wrong")
    })
	}
)

export const updatePostPrivacy = (postId, privacy, token) => (
  function(dispatch){
    let data = new FormData()
  	data.set('post_id', postId)
  	data.set('privacy', privacy)
  	axios({
      method: 'post',
      url: 'http://localhost:8000/testapp/post/changeprivacy',
      headers: {
      Authorization: 'Token '+token,
      },
      data: data
    })
    .then(response => {
      dispatch(privacyChanged(postId, privacy))
    })
    .catch(function(error){
        alert("Something Went Wrong")
    })
	}
)