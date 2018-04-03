import React, { Component } from 'react';
import { connect } from 'react-redux';
import {createPostSuccess, editPostSuccess, sortAllPosts} from '../actions';
import PostForm from '../forms/PostForm';
import ListResource from './ListResource';
import {addPost, editPost, deletePost,loadAllPosts} from '../actions/post';
import ListHeader from '../containers/ListHeader';
import Loader from '../containers/Loader';
import 'react-select/dist/react-select.css';
import Select from 'react-select';

const options = [
    { value: 'timestamp', label: 'Timestamp' },
    { value: 'voteScore', label: 'Vote Score' },
];

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
        this.props.loadAllPosts();
    }

    handleCreateSubmit(post) {
        this.props.addPost(post);
        }
    handleEditSubmit(post) {
        this.props.editPostFunc(post);
        }
    handleChange = (selectedOption) => {
        this.setState({ selectedOption });
        this.props.sortAllPosts(selectedOption.value);

    }

    render(){
        const posts= this.props.allPosts;
        const path= this.props.match.path
        const { selectedOption } = this.state;
        const value = selectedOption && selectedOption.value;

        return (

            <div className='container'>
                <Loader isFetching={this.props.isFetching}/>
                <h1>Posts</h1>
                <div className='row'>
                    <div className='col-md-6'>
                        <i  className='glyphicon glyphicon-plus'  onClick={()=> {this.props.createPostSuccess(Math.random().toString(36).slice(2))}}> </i>
                    </div>
                    <div className='col-md-4'>
                        <label>Sort</label>
                        <Select
                            name='form-field-name'
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
                        (this.props.editPostSuccess(post))
                    }
                    onDeleteClick={(post) =>
                        (this.props.deletePost(post))
                    }
                />

                {   this.props.postFormType &&
                <PostForm />

                }
            </div>

        )
    }
}
function mapStateToProps(state){

    return {
        allPosts: state.rootReducer.posts.allPosts,
        postFormType:state.rootReducer.posts.postFormType,
        isFetching:state.rootReducer.posts.isFetching
    };
}
const mapDispatchToProps = (dispatch) => {
    return {
        addPost: (post) => {
            dispatch(addPost(post))
        },
        editPostFunc: (post) => {
            dispatch(editPost(post))
        },
        deletePost:(post) => {
            dispatch(deletePost(post))
        },
        loadAllPosts:() => {
            dispatch(loadAllPosts())
        },
        sortAllPosts:(sortBy) => {
            dispatch(sortAllPosts(sortBy))
        },
        createPostSuccess:(id) => {
        dispatch(createPostSuccess(id))
    },
        editPostSuccess:(post) => {
        dispatch(editPostSuccess(post))
    },

    }
}
export default connect(mapStateToProps,mapDispatchToProps)(Posts);