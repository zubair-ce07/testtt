import React from 'react';
import { connect } from 'react-redux';
import { browserHistory } from 'react-router';
import { reduxForm, Field } from 'redux-form';
import {getCategories, addMem} from '../actions';

class TraineeSignup extends React.Component {
    componentWillMount(){
         this.props.getCategories(localStorage.getItem('token'));
        if (!localStorage.getItem('token')) {
             browserHistory.push('/');
        }
    }
    renderCategories(){
         if (this.props.categories){
        return this.props.categories.map((cat) => {
                    return <option key={cat.id} value={cat.id}> {cat.name}</option>
                });
        }
    }

    inputField(field)
    {
        return (
            <div>
                <span className="aler">{ field.meta.touched ? field.meta.error : ''}</span>
                <input
                    className="form-control"
                    type={ field.type }
                    { ...field.input }
                />

            </div>
        );
    }

    imageField(field)
    {
        return(
            <div>
                <input type="file" name="pic" accept="image/*" { ...field.input }/>
                <p className="error">{ field.meta.touched ? field.meta.error : ''}</p>
            </div>
        )
    }

    submit(values)
    {
        console.log(values);
        console.log('****************************************');
         let formData = new FormData();
         formData.append('category', values.category);
         formData.append('title', values.title);
         formData.append('text', values.text);
         formData.append('url', values.url);
         formData.append('tags', values.tags);
         formData.append('is_public', values.is_public);
         formData.append('image', values.image[0]);
       this.props.addMem(formData, localStorage.getItem('token'))
    }

    render()
    {
        const { handleSubmit }  = this.props;
        return (
                <form onSubmit={ handleSubmit(this.submit.bind(this)) }>
                    <h3>Trainer Signup</h3>
                    <div id="error-msg" hidden className="alert alert-danger">
                        <strong>Username / Password</strong>{' '}is Incorrect
                    </div>

                    <div className="form-group ">
                        <label>Catgory</label>
                        <Field name="category" component="select" className="form-control">
                            <option></option>
                            {this.renderCategories()}
                        </Field>
                    </div>

                    <div className="form-group">
                        <label>Title</label>
                        <Field type="text" name="title"  component={ this.inputField }
                               className="form-control" />
                    </div>

                    <div className="form-group">
                        <label>Text</label>
                        <Field type="text" name="text" component="textarea"
                               className="form-control" />
                    </div>

                    <div className="form-group">
                        <label>URL</label>
                        <Field type="text" name="url" component={ this.inputField }
                               className="form-control" />
                    </div>
                    <div className="form-group">
                        <label>Tags</label>
                        <Field type="text" name="tags" component={ this.inputField }
                               className="form-control" />
                    </div>
                    <div className="form-group">
                        <label for="is_public">Is_public: </label>
                        <Field  name="is_public"
                            component="input"
                            type="checkbox"
                        />
                    </div>
                    <div className="form-group">
                        <label>Image</label>
                        <Field type="file" name="image" component={ this.imageField }
                               className="form-control" />
                    </div>

                    <button type="submit" className="btn btn-primary btn-block">Submit</button>
                </form>
        )
    }
}

function validate(values)
{
    let errors = {};
    if(!values.category)
    {
        errors.category = 'Username Required';
    }
    if(!values.title)
    {
        errors.title = 'First Name Required';
    }
    if(!values.text)
    {
        errors.text = 'Last Name Required';
    }
    if(!values.url)
    {
        errors.url = 'Password Required';
    }

    return errors;
}

function mapstateToProps(state) {
    return {
        categories : state.categories
    }
}
export default reduxForm({
    form: 'TraineeSignupForm',
    validate,
})(connect(mapstateToProps, { getCategories, addMem })(TraineeSignup));
