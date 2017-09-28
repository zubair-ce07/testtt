import React, {Component} from 'react';
import { connect } from 'react-redux';
import Post from './Post'
import AddPost from './AddPost'
import { listPost, privacyChanged } from '../../actions/post'
import '../StyleSheets/PostList.css'
import axios from 'axios';


const findValueByPrefix = (object, prefix) => {
    for (var property in object) {
	    if (object.hasOwnProperty(property) && property.toString().endsWith(prefix)) {
	        return object[property];
	    }
	}
}

class PostList extends Component{

	componentDidMount(){
		/* getting user and friends posts*/
        axios({
                method: 'get',
                url: 'http://localhost:8000/testapp/post',
                headers: {
                Authorization: 'Token '+this.props.token,
                }
        })
        .then(response => {
            let data = response.data
            this.props.listPosts(data.posts, data.posts_count, data.likes_count)

        })
        .catch(function(error){
            console.log(error)
        })
	}

	updatePrivacyHandler(postId, event){
		let privacy = event.target.selectedOptions[0].id
		this.props.updatePrivacy(postId,privacy, this.props.token)
	}

	render(){
		const {posts} = this.props
		return (
			<div>
				<AddPost /><br />
				{
					posts.map( post => {
						let fileUrl = findValueByPrefix(post,"file")
						let privacyEmbed;

						if (post.user === this.props.id){
							privacyEmbed = <select onChange={this.updatePrivacyHandler.bind(this,post.id)} className="btn btn-primary"
											ref={input => {this.privacy = input}} value={post.privacy} >
												<option value="public" id="public">Public</option>	
												<option value="friends" id="friends">Friends</option>	
												<option value="only_me" id="only_me">Only Me</option>	
											</select>
						}

						return(
						<div className="postwell" key={post.id}>
							<div className="row" style={{textAlign: "right"}}>
									{privacyEmbed}		
							</div>
							<div className="row">
								<div>
									<Post id={post.id} key={post.id} caption={post.caption}
									 posted_at={post.posted_at} comments_count={post.comments_count}
									 file={fileUrl} fileType={post.file_type} postedBy={post.posted_by}
									 isLiked={post.is_liked} />
								</div>
							</div>
						</div>
						);

					})
				}
			</div>
		);
	}
}

const mapStateToProps = (state) => {
    return {
        token: state.authReducer.token,
        posts: state.postReducer.posts,
        id: state.authReducer.id
    };
}

const mapDispatchToProps = (dispatch) => {
    return {
        listPosts: (posts, posts_count, likes_count) => {
            dispatch(listPost(posts, posts_count, likes_count))
        },
        updatePrivacy: (postId, privacy, token) => {
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
		            //console.log(response.data.posts)
		            dispatch(privacyChanged(postId, privacy))

		        })
		        .catch(function(error){
		            console.log(error)
		        })
	       	}

    }
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(PostList);