import React, { Component } from 'react';
import { connect } from 'react-redux';
import {loadPosts,loadCategory} from "../actions/category";
import ListHeader from '../containers/ListHeader';
import ListResource from './ListResource';
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
                <h2>Posts</h2>
                <ListHeader mode={'category-posts'}/>

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
export default connect(mapStateToProps)(Category);