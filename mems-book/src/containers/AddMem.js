import React from 'react';
import { connect } from 'react-redux';
import { browserHistory } from 'react-router';
import { reduxForm, Field } from 'redux-form';
import {getCategories, addMem} from '../actions';

class AddMem extends React.Component {
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

    inputField(field) {
        return (
            <div >
                 <span className="alert">{ field.meta.touched ? field.meta.error : ''}</span>
                <input
                    className="form-control"
                    placeholder={field.placeholder}

                    { ...field.input }
                />

            </div>
        );
    }
    selectField(field) {
        return (
            <div >
                 <span className="alert">{ field.meta.touched ? field.meta.error : ''}</span>
                <select
                    className="form-control"

                    { ...field.input }
                >
                 <option value={''}>-- select category --</option>
                 {this.renderCategories()}
                </select>

            </div>);
    }
    textArea(field) {
        return (
            <div>
                 <span className="alert">{ field.meta.touched ? field.meta.error : ''}</span>
                <textarea
                    className="form-control"
                    placeholder={field.placeholder}

                    { ...field.input }
                />


            </div>);
    }
    imageField(field) {
        return(
            <div>

                <input type="file" name="pic" accept="image/*" { ...field.input }/>

            </div>
        )
    }

    submit(values)
    {
         let formData = new FormData();

         formData.append('category', values.category);
         formData.append('title', values.title);
         formData.append('text', values.text);
         formData.append('url', values.url);
         formData.append('tags', values.tags);
         formData.append('is_public', values.is_public);
         formData.append('image', values.image[0]);
         console.log(formData);
       this.props.addMem(formData, localStorage.getItem('token')).then(()=>{browserHistory.push('/home')})
    }

    render()
    {
        const { handleSubmit }  = this.props;
        return (
            <div className="col-md-7 col-md-offset-2">
                <form onSubmit={ handleSubmit(this.submit.bind(this)) }>
                    <center><h2> <b>Add New Mem</b> </h2></center> <br/>
                    <div className="form-group ">
                        <Field name="category" type="select" component={this.selectField.bind(this)} />


                    </div>

                    <div className="form-group">
                        <Field type="text" name="title"  placeholder="Title" component={ this.inputField }
                               className="form-control" />
                    </div>

                    <div className="form-group">
                        <Field type="text" name="text" placeholder="Text" component={this.textArea}
                               className="form-control" />
                    </div>

                    <div className="form-group">
                        <Field type="text" name="url" placeholder="Url" component={ this.inputField }
                               className="form-control" />
                    </div>
                    <div className="form-group">
                        <Field type="text" name="tags" placeholder="Tags"  component={ this.inputField }
                               className="form-control" />
                    </div>
                    <div className="form-group">
                        <div className="checkbox">
                          <label>

                            <Field
                            name="is_public"
                            component="input"
                            type="checkbox"
                          />
                                Is Public
                          </label>
                        </div>
                    </div>
                    <div className="form-group">
                        <label>Image</label>
                        <Field type="file" name="image" component={ this.imageField }
                               className="form-control" />
                    </div>

                    <button type="submit" className="btn btn-primary btn-block">Add Mem</button>
                </form>
            </div>
        )
    }
}
function validateUrl(value) {
    return /^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:[/?#]\S*)?$/i.test(value);
};
function validate(values)
{
    let errors = {};
    if(!values.category)
    {
        errors.category = 'Category Required';
    }
    if(!values.title)
    {
        errors.title = 'Title Required';
    }
    if(!values.text)
    {
        errors.text = 'Text Required';
    }
    if(!validateUrl(values.url))
    {
        errors.url = 'Url is not correct';
    }
    if(!values.tags) {
        errors.tags = 'Tags Required';
    }

    return errors;
}

function mapstateToProps(state) {
    return {
        categories : state.categories,
    }
}
export default reduxForm({
    form: 'AddMemForm',
    validate,
})(connect(mapstateToProps, { getCategories, addMem })(AddMem));
