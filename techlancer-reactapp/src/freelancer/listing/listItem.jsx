import React from 'react';
import PropTypes from 'prop-types'
import freelancer_image from '../../images/freelancer.png'

export default class ListItem extends React.Component {
	static propTypes = {
		username: PropTypes.string,
	};

	constructor(props) {
		super(props);
		this.state={
			username:props.username
		}
	}

	render() {
		return (
			    <a href="#">
					<img src="{freelancer_image}" alt="" className="img-circle img-responsive"/>
					<div className="title">
						<h5>{this.state.username}</h5>
					</div>
				</a>
		);
	}
}
