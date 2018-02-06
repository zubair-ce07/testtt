import React from 'react';
import PropTypes from 'prop-types'

export default class Signup_Form extends React.Component {
    static propTypes = {
    onSubmit: PropTypes.func.isRequired,
    onChange: PropTypes.func.isRequired,
    errors: PropTypes.object.isRequired,
    user: PropTypes.object.isRequired
    };
    constructor(props) {
            super(props);
            this.onSubmit = props.onSubmit;
            this.onChange = props.onChange;
            this.errors = props.errors;
            this.user = props.user;
        }
    render() {
        return (
            <form onSubmit={this.onSubmit}>
            <div className="row">
                <div className="form-group col-md-12">
                    <label className="col-md-3 control-lable" forHtml="lastName">Username</label>
                    <div className="col-md-9">
                        <input type="text" name="name"
                         id="name" className="form-control input-sm"
                        onChange={this.onChange}/>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="form-group col-md-12">
                    <label className="col-md-3 control-lable" forHtml="email">Password</label>
                    <div className="col-md-9">
                        <input type="password" id="password" name="password" 
                        className="form-control input-sm" onChange={this.onChange}/>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="form-group col-md-12">
                    <label className="col-md-3 control-lable" forHtml="email">Confirm Password</label>
                    <div className="col-md-9">
                        <input type="password" id="password" 
                        name="confirm_password" className="form-control input-sm"
                        onChange={this.onChange}/>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="form-actions floatRight">
                    <input type="submit" value="Register" className="btn btn-primary btn-sm"/>
                </div>
            </div>
        </form>
        );
    }
}
