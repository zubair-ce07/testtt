import React from 'react';
import { connect } from 'react-redux';
import { Link, browserHistory } from 'react-router';

import { fetchBlog } from '../actions/retrieve_blog';
import { deleteBlog } from '../actions/delete_blog_post';

class BlogDetails extends React.Component
{
    componentWillMount()
    {
        this.props.fetchBlog(this.props.params.id);
    }

    deletePost()
    {
        this.props.deleteBlog(this.props.params.id).then(() => {
            browserHistory.push("/");
        });
    }

    render()
    {
        if(!this.props.blog)
        {
            return (<div>Loading...</div>)
        }
        else
        {
            return (
                <div>
                    <button type="submit" className="btn btn-danger pull-xs-right"
                            onClick={this.deletePost.bind(this)}>Delete Blog</button>

                    <Link to="/">Back to Index</Link>
                    <h3>{ this.props.blog.title }</h3>
                    <h6>Categories: { this.props.blog.categories }</h6>
                    <p>{this.props.blog.content}</p>
                </div>
            )
        }
    }
}

function mapStateToProps(state)
{
    return { blog: state.blog_details.post };
}

export default connect(mapStateToProps, { fetchBlog, deleteBlog })(BlogDetails);