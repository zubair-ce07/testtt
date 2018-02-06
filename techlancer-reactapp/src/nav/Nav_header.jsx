import React from 'react';
import PropTypes from 'prop-types';
import logo from '../images/logo1.png';


export default class NavHeader extends React.Component {
    static propTypes = {
        name: PropTypes.string,
    };
    render() {
        return (
            <div className="navbar-header">
                <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span className="sr-only">Toggle navigation</span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                </button>
                <a className="navbar-brand" href="index.html"><img src={logo} alt=""/></a>
            </div>
        );
    }
}
