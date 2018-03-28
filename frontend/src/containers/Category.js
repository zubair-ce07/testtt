import React, { Component } from 'react';
import { connect } from 'react-redux';
import {loadPosts,loadCategory} from "../actions/category";

class Category extends Component {

    componentDidMount() {
        this.props.dispatch(loadPosts(this.props.match.params.category));

    }
    componentWillReceiveProps(nextProps){

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
              </div>
        )
    }
}
function mapStateToProps(state){
    return {
        posts: state.rootReducer.posts.posts,
        categories: state.rootReducer.categories.categories
    };
}
export default connect(mapStateToProps)(Category);