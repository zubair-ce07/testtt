import React, {Component} from 'react';
import FollowPlayersList from './FollowPlayersList';
import PLAYERS from '../PlayersData';

class FollowPlayers extends Component {
  constructor(props) {
    super(props);
    this.state = {players: PLAYERS};

  }

  render() {
    return (
      <div>
        <h1>Follow Players</h1>
        <FollowPlayersList players={this.state.players}/>
      </div>
    );
  }
}

export default FollowPlayers;
