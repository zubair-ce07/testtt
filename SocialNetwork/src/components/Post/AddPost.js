import React from 'react'
import {connect} from 'react-redux';
import {addPostApi} from '../../actions/post'
import '../StyleSheets/PostList.css'

const AddPost = ({addPostClicked, token}) => {
	let caption;
	let file;
	let privacy;
	return (
		<div className="postwell">
			<div className="row" style={{textAlign: "right"}}>
				<select 
					className="btn btn-primary" 
					ref={input => {privacy= input}} 
					style={{marginLeft: "50%"}}>
						<option id="public">Public</option>	
						<option id="friends">Friends</option>	
						<option id="only_me">Only Me</option>	
				</select>
			</div>
			<div className="row">
				<h4>Add post</h4>	
				<textarea 
					className="form-control" 
					placeholder="Write post caption here..." 
					ref={(input) => { caption = input }} 
				/>
				<br />
				<input 
					style={{padding: "5px"}} 
					type="file" 
					ref={(input) => { file = input } } 
				/>
				<br />
				<button 
					className="btn btn-default" 
					onClick={() => addPostClicked(caption, file, token, privacy.selectedOptions[0].id)}>
					Add Post
				</button>
			</div>
		</div>
	);
}

const mapStateToProps = (state) => ({
	token: state.authReducer.token
})

const mapDispatchToProps = (dispatch) => ({
	addPostClicked: (caption, file, token, privacy) => {
		const ext = file.value.substr(file.value.lastIndexOf('.') + 1);
		let fileType;
		
		if (ext === "mp3" || ext === "wav"){
			fileType = "audio"
		}
		else if(ext === "mp4" || ext === "flv" || ext === "mpeg"){
			fileType = "video"
		}
		else if(ext === "jpg" || ext === "png")
		{
			fileType = "image"
		}

		dispatch(addPostApi(caption, file, token, privacy, fileType))
    caption.value = ''
		file.value = ''
	}
})

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(AddPost)