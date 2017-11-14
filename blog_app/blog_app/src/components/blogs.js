import React from 'react';
import { fetchBlogPosts } from '../actions/retrieve_all_blogs';
import { connect } from 'react-redux';
import { Link } from 'react-router';

class BlogsIndex extends React.Component
{
    componentWillMount()
    {
        this.props.fetchBlogPosts();
    }

    renderPosts()
    {
        if (this.props.blogs.results)
        {
            return (
                this.props.blogs.results.map(blog => {
                    return (
                        <li className="list-group-item" key={ blog.id }>
                            <Link to={ "post/" + blog.id }>
                                <span className="pull-xs-right">{ blog.categories }</span>
                                <strong>{ blog.title }</strong>
                            </Link>
                        </li>
                    )
                })
            );
        }
        else
        {
            return <div>Loading...</div>
        }
    }

    render()
    {
        return (
            <div>
                <div className="text-xs-right">
                    <Link to="/post/new" className="btn btn-primary">
                        Add Post
                    </Link>
                </div>
                <h3>Blogs</h3>
                <ul className="list-group">
                    { this.renderPosts() }
                </ul>
            </div>
        );
    }
}

function mapStateToProps(state)
{
    return {'blogs': state.blogs.all };
}

export default connect(mapStateToProps, { fetchBlogPosts })(BlogsIndex);