import React, { Component } from 'react';
import { connect } from 'react-redux';
import {loadAllPosts} from "../actions/category";
import Post from '../containers/Post';
import {
    BrowserRouter as Router,
    Link,
    Route // for later
} from 'react-router-dom'
class Posts extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        console.log(this.props)
        this.props.dispatch(loadAllPosts());
    }

    render(){
        const posts= this.props.allPosts;
        const url= this.props.match.url
        return (

            <div className='container'>
                <h1>Posts1</h1>

                <ul>
                    {posts.map(function(post){
                       return <li key={post.id}>
                            <Link to={`${url}/${post.id}`}>{post.title}</Link>
                        </li>

                    })}
                </ul>
                <Route path={`${url}/:post`} component={Post}/>



            </div>

        )
    }
}
function mapStateToProps(state){
    console.log(state)
    return {
        allPosts: state.rootReducer.data.allPosts,
        posts: state.rootReducer.data.posts,
        categories: state.rootReducer.data.categories
    };
}
export default connect(mapStateToProps)(Posts);