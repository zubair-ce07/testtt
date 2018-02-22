import React from 'react';
import PropTypes from 'prop-types';

export default class ListItem extends React.Component {
  static propTypes = {
    username: PropTypes.string
  };

  constructor(props) {
    super(props);
    this.state={
      username:props.username, 
    }
  }

  render() {
    return (
      <a href="#">
        <div className="title">
          <h5>{this.state.username}</h5>
        </div>
      </a>
    );
  }
}
