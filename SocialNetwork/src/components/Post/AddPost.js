import React from 'react'
import {connect} from 'react-redux';
import '../StyleSheets/PostList.css'
import {addPost} from '../../actions/post'
import axios from 'axios'

const AddPost = ({addPostClicked, token}) => {
	let caption;
	let file;
	let privacy;
	return (
		<div className="postwell">
			<div className="row" style={{textAlign: "right"}}>
					<select className="btn btn-primary" ref={input => {privacy= input}} style={{marginLeft: "50%"}}>
						<option id="public">Public</option>	
						<option id="friends">Friends</option>	
						<option id="only_me">Only Me</option>	
					</select>
			</div>
			<div className="row">
				<h4>Add post</h4>	
				<textarea className="form-control" placeholder="Write post caption here..." ref={(input) => { caption = input }} /><br />
				<input className="" style={{padding: "5px"}} type="file" ref={(input) => { file = input } } />

				<br />
				<button className="btn btn-default" onClick={() => addPostClicked(caption, file, token, privacy.selectedOptions[0].id)} >Add Post</button>
			</div>
		</div>
	);
}

const mapStateToProps = (state) => {
	return {
		token: state.authReducer.token
	};
}

const mapDispatchToProps = (dispatch) => {
	return {
		addPostClicked: (caption,file, token, privacy) => {
			let ext = file.value.substr(file.value.lastIndexOf('.') + 1);
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
	            console.log(error)
	            alert("Post not created.")
	        })

	        caption.value = ''
			file.value = ''

		}
	};
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(AddPost)