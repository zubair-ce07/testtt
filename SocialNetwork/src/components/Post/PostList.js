import React, {Component} from 'react';
import { connect } from 'react-redux';
import Post from './Post'
import AddPost from './AddPost'
import { fetchPosts, updatePostPrivacy } from '../../actions/post'
import '../StyleSheets/PostList.css'


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
		this.props.fetchedPosts(this.props.token)
        
	}

	updatePrivacyHandler(postId, event){
		let privacy = event.target.selectedOptions[0].id
		this.props.updatePrivacy(postId,privacy, this.props.token)
	}

	render(){
		const {posts} = this.props
		return (
			<div>
				<AddPost />
				<br />
				{
					posts.map( post => {
						const fileUrl = findValueByPrefix(post,"file")
						let privacyEmbed;

						if (post.user === this.props.id){
							privacyEmbed = (
								<select 
									onChange={this.updatePrivacyHandler.bind(this,post.id)} 
									className="btn btn-primary"
									ref={input => {this.privacy = input}} value={post.privacy} >
										<option value="public" id="public">Public</option>	
										<option value="friends" id="friends">Friends</option>	
										<option value="only_me" id="only_me">Only Me</option>	
								</select>
							);
						}

						return (
							<div className="postwell" key={post.id}>
								<div className="row" style={{textAlign: "right"}}>
										{privacyEmbed}		
								</div>
								<div className="row">
									<div>
										<Post 
											id={post.id} 
											key={post.id} 
											caption={post.caption}
										 	posted_at={post.posted_at} 
										 	comments_count={post.comments_count}
										 	file={fileUrl} 
										 	fileType={post.file_type} 
										 	postedBy={post.posted_by}
										 	isLiked={post.is_liked} 
										/>
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

const mapStateToProps = (state) => ({
  token: state.authReducer.token,
  posts: state.postReducer.posts,
  id: state.authReducer.id
})

const mapDispatchToProps = (dispatch) => ({
	fetchedPosts: (token) =>{
		dispatch(fetchPosts(token))
	},
    updatePrivacy: (postId, privacy, token) => {
    	dispatch(updatePostPrivacy(postId, privacy, token))	
    }
})

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(PostList);