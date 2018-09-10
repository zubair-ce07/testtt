import React from 'react';
import {ListGroupItem} from 'react-bootstrap';

const TeamsListItem = (props) => {
  const team = props.team;

  if(!team) {
    return <div>Team Not found</div>;
  }

  const url = team.url;
  const name = team.name;

  return (
    <li className="list-group-item">
      <a href={url}>{name}</a>
    </li>
  );
}

export default TeamsListItem;
