import { Link } from 'react-router-dom';
import React from 'react';

import PropTypes from 'prop-types'

// import {
//   Link,
// } from 'react-router-dom'

export default class Menu extends React.Component {
	static propTypes = {
		name: PropTypes.string,
	};
	render() {
		return (
			<div className="navbar-collapse collapse" id="bs-example-navbar-collapse-1" style={{height: 1 +'px'}}>
		        <ul className="nav navbar-nav">
			        <li>
			        	<Link to="/login">Login</Link>
			        </li>
		        </ul>
		    </div>
		);
	}
}

