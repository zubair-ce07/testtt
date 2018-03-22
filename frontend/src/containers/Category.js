import React, { Component } from 'react';
import { connect } from 'react-redux';
import {loadPosts,loadCategory} from "../actions/category";
import Post from '../containers/Post';
import {
    BrowserRouter as Router,
    Link,
    Route // for later
} from 'react-router-dom'
class Category extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        console.log(this.props)
        this.props.dispatch(loadPosts(this.props.match.params.category));

    }
    componentWillReceiveProps(nextProps){
        console.log(nextProps)
        if(!nextProps.categories.length) this.props.dispatch(loadCategory())
        if(nextProps.match.params.category!==this.props.match.params.category)  this.props.dispatch(loadPosts(nextProps.match.params.category));

    }

    render(){
        const posts= this.props.posts;
        return (
            <div className='container'>
                <h1>Posts</h1>

                <ul>
                    {posts.map(function(post){
                         return <li key={post.id} >{post.title}</li>
                    })}

                </ul>
                <hr />



            </div>
        )
    }
}
function mapStateToProps(state){
    console.log(state)
    return {
        posts: state.rootReducer.data.posts,
        categories: state.rootReducer.data.categories
    };
}
export default connect(mapStateToProps)(Category);