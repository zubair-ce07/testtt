import React from 'react';
import { reduxForm, Field } from 'redux-form';
import { toastr } from 'react-redux-toastr';
import { connect } from 'react-redux';

import { searchUsers } from '../actions/search_users';
import { browserHistory } from "react-router";


class SearchBar extends React.Component
{
    searchField(field)
    {
        return (
            <div id="text">
                <div className="input-group">
                    <input type="text" className="form-control" placeholder="Search"
                           { ...field.input }/>
                    <div className="input-group-btn">
                        <button className="btn btn-default" type="submit"
                            onClick={() => {
                                if (field.meta.touched && field.meta.error)
                                    toastr.error('Query Error', field.meta.error)
                            }}>
                            <i className="glyphicon glyphicon-search"/>
                        </button>
                    </div>
                </div>
            </div>
        )
    }

    submit(values)
    {
        this.props.searchUsers(values.search)
        .then(response => {
            browserHistory.push(`/search/${values.search}`);
        })
        .catch(error => {
            console.log(error);
        })
    }

    render()
    {
        const { handleSubmit }  = this.props;
        return (
            <form className="navbar-form navbar-left" onSubmit={ handleSubmit(this.submit.bind(this)) }>
                <Field component={ this.searchField } name="search" />
            </form>
        );
    }
}

function validate(values)
{
    let errors = {};

    if(!values.search)
    {
        errors.search = 'Enter Search Field';
    }

    return errors;
}

export default reduxForm({
        form: 'SearchForm',
        validate
})(connect(null, { searchUsers })(SearchBar));