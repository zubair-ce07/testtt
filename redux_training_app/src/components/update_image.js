import React from 'react';
import { reduxForm, Field } from 'redux-form';
import { connect } from 'react-redux';
import { updateImage } from '../actions/update_image';
import _ from 'lodash';

class ImageUpdation extends React.Component
{
    updateImage(values)
    {
        this.props.updateImage(values);
    }

    imageField(field)
    {
        return (
            <div className="form-group">
                {
                    field.meta.error && field.meta.touched
                    ? <div className="alert alert-danger">
                        {field.meta.error}
                      </div>
                    : <div/>
                }
                <input className="form-control"
                       type={ field.type }
                       accept="image/*"
                       value={ null }
                       { ...field.input }
                />
            </div>
        );
    }

    render()
    {
        const { handleSubmit }  = this.props;
        return (
            <form onSubmit={ handleSubmit(this.updateImage.bind(this)) }>

                <Field type="file" name="picture" component={ this.imageField }
                       className="form-control" />

                <input className="form-control" type="submit"
                       value="Update Image"/>
            </form>
        )
    }
}

function validate(values)
{
    let errors = {};

    console.log(values.picture);

    if(_.isEmpty(values.picture))
    {
        errors.picture = 'Select an image first';
    }
    return errors;
}

export default reduxForm({
    form: 'ImageUpdateForm',
    validate,
})(connect(null, { updateImage })(ImageUpdation));