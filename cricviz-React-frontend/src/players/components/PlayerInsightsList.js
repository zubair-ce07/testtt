import React, {Component} from 'react';
import {ListGroup, ListGroupItem} from 'react-bootstrap';
import PlayerInsightsListItem from './PlayerInsightsListItem';
import PLAYERS from '../PlayersData';

const PlayerInsightsList = (props) => {
  const AllPlayers = props.players.map((player) => {
    return (
      <PlayerInsightsListItem
        key={player.url}
        player={player} />
      );
    });

  return (
    <ul className="col-md-6 list-group">
      {AllPlayers}
    </ul>
  );
}

export default PlayerInsightsList;
