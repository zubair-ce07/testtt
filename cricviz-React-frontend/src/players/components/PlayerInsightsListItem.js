import React from 'react';
import {ListGroupItem} from 'react-bootstrap';

const PlayerInsightsListItem = (props) => {
  const player = props.player;

  if(!player) {
    return <div>Player Not found</div>;
  }

  const url = player.url;
  const name = player.name;

  return (
    <li className="list-group-item">
      <a href={url}>{name}</a>
    </li>
  );
}

export default PlayerInsightsListItem;
