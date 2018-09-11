import React, {Component} from 'react';
import TeamsList from './TeamsList';
import TEAMS from '../TeamsData';
import FollowTeamsList from './FollowTeamsList';

class FollowTeams extends Component {
  constructor(props) {
    super(props);
    this.state = {teams: TEAMS};

  }

  render() {
      return (
        <div>
          <h1>Popular International Teams</h1>
          <h3>Select a team to follow</h3>
          <FollowTeamsList teams={this.state.teams}/>
        </div>
      );
    }
}

export default FollowTeams;
