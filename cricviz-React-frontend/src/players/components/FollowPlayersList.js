import React, {Component} from 'react';
import {ListGroup, ListGroupItem} from 'react-bootstrap';
import FollowPlayersListItem from './FollowPlayersListItem';
import PLAYERS from '../PlayersData';

const FollowPlayersList = (props) => {
  const AllPlayers = props.players.map((player) => {
    return (
      <FollowPlayersListItem
        key={player.url}
        player={player} />
      );
    });

  return (
    <ul className=" col-md-6 list-group">
      {AllPlayers}
    </ul>
  );
}

export default FollowPlayersList;
