import React, {Component} from 'react';
import TeamsList from './TeamsList';
import axios from 'axios';
import TEAMS from '../TeamsData';

class TeamsHome extends Component {
  constructor(props) {
    super(props);
    this.state = {teams: TEAMS};

  }

  render() {
      // GET request for remote data
        axios({
            method:'get',
            url:'http://127.0.0.1:8000/teams/',
            json: true,
            })
        .then(function(response) {
          console.log(response.data.results);
        });

      return (
        <div>
          <h1>Cricket Teams Index (Popular International Teams)</h1>
          <TeamsList teams={this.state.teams}/>
        </div>
      );
    }
}

export default TeamsHome;
