import React, { Component } from 'react';
import { connect } from 'react-redux';
import {loadPosts} from '../actions/category';
import ListHeader from '../containers/ListHeader';
import ListResource from './ListResource';
class Category extends Component {

    componentDidMount() {
        this.props.loadPosts(this.props.match.params.category);

    }
    componentWillReceiveProps(nextProps){
        if(nextProps.match.params.category!==this.props.match.params.category)  {
            this.props.loadPosts(nextProps.match.params.category);
        }

    }

    render(){
        const posts= this.props.posts;
        return (


            <div className='container'>
                <h2>Posts</h2>
                {
                    Boolean(posts.length) &&
                    <ListHeader mode={'category-posts'}/>
                }
                <ListResource
                    resource={posts}
                    mode={'category-posts'}
                />
              </div>
        )
    }
}
function mapStateToProps(state){
    return {
        posts: state.rootReducer.categories.posts,
        categories: state.rootReducer.categories.categories
    };
}
const mapDispatchToProps = (dispatch) => {
    return {
        loadPosts: (category) => {
            dispatch(loadPosts(category))
        },

    }
}
export default connect(mapStateToProps,mapDispatchToProps)(Category);