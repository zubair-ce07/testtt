import React from 'react';
import {ListGroupItem} from 'react-bootstrap';

const FollowPlayersListItem = (props) => {
  const player = props.player;

  if(!player) {
    return <div>Player Not found</div>;
  }

  const url = player.url;
  const name = player.name;
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

export default FollowPlayersListItem;
