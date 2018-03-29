import React, { Component } from 'react';
import { connect } from 'react-redux';
import {loadPost} from '../actions/post';
import Comments from '../containers/Comments'
import Timestamp from 'react-timestamp';

class Post extends Component {

    componentDidMount() {
        this.props.loadPost(this.props.match.params.post);
    }
    componentWillReceiveProps(nextprops) {

        if(nextprops.match.params.post!==this.props.match.params.post)
        this.props.loadPost(this.props.match.params.post);

    }

    render(){
        const post= this.props.post;
        return (

            <div className='container'>
                <h2>{post.title}</h2>
                <div className={'row'}>
                    <div className={'col-md-6'}>
                        <b>Detail </b>{post.body}
                    </div>
                    <div className={'col-md-3'}>
                        <b>Author </b>{post.author}
                    </div>
                    <div className={'col-md-2'}>
                        <b>Time </b><Timestamp time={post.timestamp}/>
                    </div>
                    <div className={'col-md-1'}>
                        <b>Votes  </b>{post.voteScore}
                    </div>

                </div>
                <Comments />
            </div>

        )
    }
}
function mapStateToProps(state){
    return {
        post:state.rootReducer.posts.post
    };
}
const mapDispatchToProps = (dispatch) => {
    return {
        loadPost: () => {
            dispatch(loadPost())
        }
    }
}

export default connect(mapStateToProps,mapDispatchToProps)(Post);