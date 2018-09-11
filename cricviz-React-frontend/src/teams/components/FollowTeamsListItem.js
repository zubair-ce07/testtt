import React from 'react';
import {ListGroupItem} from 'react-bootstrap';

const FollowTeamsListItem = (props) => {
  const team = props.team;

  if(!team) {
    return <div>Team Not found</div>;
  }

  const url = team.url;
  const name = team.name;

  const styles = {
    marginLeft: '100px',
    display: 'inline'
  };

  return (
    <li className="list-group-item">
      <a href={url}>{name}</a>
      <button type="button" className="btn btn-info" style={styles}>Follow</button>
    </li>
  );
}

export default FollowTeamsListItem;
