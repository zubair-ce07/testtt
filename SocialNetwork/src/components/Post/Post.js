import React, {Component} from 'react';
import CommentList from '../Comment/CommentList';
import LikeList from '../Like/LikeList'
import AddLike from '../Like/AddLike'
import {connect} from 'react-redux';
import {fetchComments} from '../../actions/comment'
import {fetchLikes} from '../../actions/like'


const VideoEmbed = ({file}) => (
  <video 
    width="320" 
    height="240"  
    controls>
    <source 
      src={"http://localhost:8000"+file} 
      type="video/mp4">
    </source>
    Your browser does not support the video tag.
  </video>
)

const AudioEmbed = ({file}) => (
  <audio controls>
    <source 
      src={"http://localhost:8000"+file} 
      type="audio/mpeg">
    </source>
    Your browser does not support the video tag.
  </audio>
)

const ImageEmbed = ({file}) => (
  <img 
    width="320" 
    height="240" 
    src={"http://localhost:8000"+file} 
    alt="post">
  </img>
)

class Post extends Component{
	constructor(props){
		super(props)

		this.state = {showComments: false, showLikes: false}
		this.showComments = this.showComments.bind(this)
		this.hideComments = this.hideComments.bind(this)

		this.showLikes = this.showLikes.bind(this)
		this.hideLikes = this.hideLikes.bind(this)

	}

	showComments(e){
		let fetched_comments = this.props.comments
		let has_fetched = false
		fetched_comments.forEach(commentsById => {
			if (Object.keys(commentsById)[0] === e.target.id){
				has_fetched = true
			}
		})

		if (has_fetched === false)
		{
			this.props.fetchPostComments(e.target.id, this.props.token)
        }
        
		this.setState({showComments: true})
		
	}

	hideComments(e){
		this.setState({showComments: false})
	}

	showLikes(e){

		let fetched_likes = this.props.likes
		let has_fetched = false
		fetched_likes.forEach(likesById => {
			if (Object.keys(likesById)[0] === e.target.id){
				has_fetched = true
			}
		})
		if (has_fetched === false)
		{
			this.props.fetchPostLikes(e.target.id, this.props.token)
        }
		this.setState({showLikes: true})
		
	}

	hideLikes(e){
		this.setState({showLikes: false})
	}

	render(){
		const {caption , comments_count, posted_at, postedBy, id, comments, file, fileType, likes, isLiked } = this.props;
		let hidn_n_show_comment;
		let post_realted_comments = [];
		let key;

		let hidn_n_show_likes;
		let post_realted_likes = [];

		comments.forEach( i => {
 			key = Object.keys(i)[0]
 			if (parseInt(key,10) === id){
 				post_realted_comments = Object.values(i)[0]
 			}
		})

		likes.forEach( i => {
			key = Object.keys(i)[0]
			if (parseInt(key,10) === id){
 				post_realted_likes = Object.values(i)[0]
 			}
		})

		/*** Conditions for show or hide comments ***/
		if(this.state.showComments === true){
			hidn_n_show_comment = ( 
				<div>
					<button 
						id={id} 
						className="btn btn-primary" 
						onClick={ this.hideComments } >
						Hide Comments
					</button>
					<CommentList 
						comments={post_realted_comments} 
						postId={id}
					/>
				</div>
			);
		}
		else{
			hidn_n_show_comment = ( 
				<button 
					id={id} 
					className="btn btn-primary" 
					onClick={ this.showComments }>
					Show Comments
				</button>
			);						
		}

		/*** Conditions for show or hide likes ***/
		if(this.state.showLikes === true){
			hidn_n_show_likes = ( 
				<div>
					<button 
						id={id} 
						className="btn btn-primary" 
						onClick={ this.hideLikes }>
						Hide Likes
					</button>
					<LikeList 
						likes={post_realted_likes} 
					/>
				</div>
			);
		}
		else{
			hidn_n_show_likes = (
				<button 
					id={id} 
					className="btn btn-primary" 
					onClick={ this.showLikes }>
					Show Likes
				</button>
			);
		}

		/*** Conditions for post type ***/
		let postEmbed;
		if(fileType === "video"){
			postEmbed = ( 
				<VideoEmbed file={file} />
			);
		}
		else if (fileType === "audio" ){
			postEmbed = ( 
				<AudioEmbed file={file} />
			);	
		}
		else{
			postEmbed = ( 
				<ImageEmbed file={file} />
			);
		}

		return (
			<div >
				{postEmbed}
				<p>{caption}</p><br/>
				<p>Number of comments on this post: {comments_count}</p>
				<p>Posted at {posted_at}</p> <br />
				<p>Posted by { postedBy }</p><br />
				<div className="row">
					<div className="col-lg-4">
						{hidn_n_show_comment}
					</div>
					<div className="col-lg-4">
						{hidn_n_show_likes}
					</div>
					<div className="col-lg-4">
						<AddLike 
							isLiked={isLiked} 
							postId={id}
						/>
					</div>
				</div>
			</div>
		);
	}
}


const mapStateToProps = (state) => ({
  isLoggedIn: state.authReducer.isLoggedIn,
  username: state.authReducer.username,
  token: state.authReducer.token,
  comments: state.commentReducer.comments,
  likes: state.likeReducer.likes,
})

const mapDispatchToProps = (dispatch) => ({
  fetchPostComments: (postId, token) => {
  	dispatch(fetchComments(postId, token))
  },
  fetchPostLikes: (postId, token) => {
  	dispatch(fetchLikes(postId, token))
  }
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Post);