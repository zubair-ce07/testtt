import React, { Component } from 'react';
import { connect } from 'react-redux';
import {createPostSuccess, editPostSuccess, sortAllPosts} from "../actions";
import PostForm from "../forms/PostForm";
import ListResource from "./ListResource";
import {addPost, editPost, deletePost,loadAllPosts} from "../actions/post";
import Select from 'react-select';
import ListHeader from '../containers/ListHeader'

import 'react-select/dist/react-select.css';
const options = [
    { value: 'timestamp', label: 'Timestamp' },
    { value: 'voteScore', label: 'Vote Score' },
]

class Posts extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedOption: '',
        }

        this.handleCreateSubmit = this.handleCreateSubmit.bind(this);
        this.handleEditSubmit = this.handleEditSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    componentDidMount() {
        this.props.dispatch(loadAllPosts());
    }

    handleCreateSubmit(post) {
        this.props.dispatch(addPost(post));
        }
    handleEditSubmit(post) {
        this.props.dispatch(editPost(post));
        }
    handleChange = (selectedOption) => {
        this.setState({ selectedOption });
        this.props.dispatch(sortAllPosts(selectedOption.value));

    }

    render(){
        const posts= this.props.allPosts;
        const path= this.props.match.path
        const { selectedOption } = this.state;
        const value = selectedOption && selectedOption.value;

        return (

            <div className='container'>
                <h1>Posts</h1>
                <div className={'row'}>
                    <div className={'col-md-6'}>
                        <i  className={'glyphicon glyphicon-plus'}  onClick={()=> {this.props.dispatch(createPostSuccess())}}> </i>
                    </div>
                    <div className={'col-md-4'}>
                        <label>Sort</label>
                        <Select
                            name="form-field-name"
                            value={value}
                            onChange={this.handleChange}
                            options={options}
                        />
                    </div>
                </div>
                <ListHeader resource={'post'}/>

                <ListResource
                    resource={posts}
                    path={path}
                    mode={'posts'}
                    onEditClick={(post) =>
                        (this.props.dispatch(editPostSuccess(post)))
                    }
                    onDeleteClick={(post) =>
                        (this.props.dispatch(deletePost(post)))
                    }
                />

                {   this.props.createPost &&
                <PostForm mode={'create'} onSubmit={this.handleCreateSubmit}/>

                }
                {   this.props.editPost &&
                <PostForm mode={'edit'} onSubmit={this.handleEditSubmit}/>
                }
            </div>

        )
    }
}
function mapStateToProps(state){

    return {
        allPosts: state.rootReducer.posts.allPosts,
        createPost:state.rootReducer.posts.createPost,
        editPost:state.rootReducer.posts.editPost
    };
}
export default connect(mapStateToProps)(Posts);