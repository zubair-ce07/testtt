import _ from 'lodash';
import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Field, reduxForm} from 'redux-form';
import {Button, Modal, ModalHeader, ModalBody, UncontrolledAlert} from 'reactstrap';

import {updateUser} from '../actions/user_actions';


class UserUpdateModal extends Component {
    constructor(props) {
        super(props);
        this.state = {
            modal: false,
            errors: null
        };

        this.toggle = this.toggle.bind(this);
    }
    onSubmit(values) {
        this.setState({'errors': null});
        this.props.updateUser(values, this.props.user).then(
            (res) => {
                this.toggle();
            },
            (err) => {
                this.setState({'errors': err.response.data});
            });
    }

    renderErrors() {
        return _.map(this.state.errors, (value, key) => {
            return <UncontrolledAlert color="warning" key={key}>{value}</UncontrolledAlert>
        });
    }

    toggle() {
        this.setState({
            modal: !this.state.modal
        });
    }

    render() {
        const handleSubmit = this.props.handleSubmit;
        return (
            <div>
                <Button className="btn btn-secondary update-btn" onClick={this.toggle}>
                    <i className="fa fa-pencil"/> {this.props.buttonLabel}
                </Button>

                <Modal isOpen={this.state.modal} toggle={this.toggle} backdrop="static">
                    <ModalHeader toggle={this.toggle}>Update User</ModalHeader>

                    <ModalBody>
                        {this.renderErrors()}
                        <form onSubmit={handleSubmit(this.onSubmit.bind(this))}>
                            <Field label="Password" name="password" type="password" component={renderField}/>
                            <Field label="Profile Photo" name="photo" type="file" component={renderField}/>
                            <button type="submit" className="btn btn-secondary float-right">
                                <i className="fa fa-pencil"/> {this.props.buttonLabel}
                            </button>
                        </form>
                    </ModalBody>
                </Modal>
            </div>
        );
    }
}

function validate(values) {
    const errors = {
        password: "Enter password or select a photo",
        photo: "Enter password or select a photo"
    };
    if (values.password || (values.photo && values.photo[0])) {
        errors.password = "";
        errors.photo = "";
    }
    return errors;
}

function renderField(field) {
    const {meta: {touched, error}} = field;
    const className = `form-group ${touched && error ? 'has-error has-feedback' : touched ? 'has-success has-feedback' : ''}`;
    let input = null;
    if (field.type === "file")
        input = <input className="form-control" type={field.type} accept="image/*" {...field.input} value={undefined}/>;
    else
        input = <input className="form-control" type={field.type} {...field.input} />;
    return (
        <div className={className}>
            <label className="control-label">{field.label}</label>
            {input}
            <div className="text-warning">
                {touched ? error : ''}
            </div>
        </div>
    );
}

export default reduxForm({
    destroyOnUnmount: false,
    validate,
    form: 'UserUpdateForm'
})(
    connect(null, {updateUser})(UserUpdateModal)
);
