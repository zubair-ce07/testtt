import React from 'react';
import { reduxForm, Field } from 'redux-form';
import { Link, browserHistory } from 'react-router';

import { createBlogPost } from '../actions/create_blog_post';

class NewBlogPost extends React.Component
{
    inputField(field){
        return (
            <div className="form-group">
                <label>{field.label}</label>
                <input
                    className="form-control"
                    type="text"
                    {...field.input}
                />
                <p className="error">{ field.meta.touched ? field.meta.error : ''}</p>
            </div>
        );
    }

    textArea(field){
        return (
            <div className="form-group">
                <label>{field.label}</label>
                <textarea
                    className="form-control"
                    type="text"
                    {...field.input}
                />
                <p className="error">{ field.meta.touched ? field.meta.error : ''}</p>
            </div>
        );
    }

    render()
    {
        const { handleSubmit }  = this.props;
        return (
            <form onSubmit={handleSubmit}>
                <h3>Create A New Blog Post</h3>
                <div className="form-group ">
                    <label>Title</label>
                    <Field type="text" name="title" component={ this.inputField }
                           className="form-control" />
                </div>

                <div className="form-group">
                    <label>Categories</label>
                    <Field type="text" name="categories" component={ this.inputField }
                           className="form-control" />
                </div>

                <div className="form-group">
                    <label>Content</label>
                    <Field type="text" name="content" component={ this.textArea }
                           className="form-control" />
                </div>

                <button type="submit" className="btn btn-primary">Submit</button>
                {' '}
                <Link to="/" className="btn btn-danger">Cancel</Link>
            </form>
        );
    }
}

function validate(values)
{
    let errors = {};

    if(!values.title)
    {
        errors.title = 'Title Required';
    }

    if(!values.categories)
    {
        errors.categories = 'Categories Required';
    }

    if(!values.content)
    {
        errors.content = 'Some Content Required';
    }

    return errors;
}

export default reduxForm({
    form: 'NewBlogPostForm',
    validate: validate,
    onSubmit: (values) => {
        createBlogPost(values).payload
            .then(() => {
            browserHistory.push("/");
        });
    }
}
,)(NewBlogPost);