import React, {Component} from 'react';
import TeamsList from './TeamsList';
import axios from 'axios';

const TEAMS = [
  {
    url: 'http://www.espncricinfo.com/team/_/id/1/england/',
    name: 'England',
  },
  {
    url: 'http://www.espncricinfo.com/team/_/id/2/australia/',
    name: 'Australia',
  },
  {
    url: 'http://www.espncricinfo.com/team/_/id/7/pakistan/',
    name: 'Pakistan',
  },
  {
    url: 'http://www.espncricinfo.com/team/_/id/6/india/',
    name: 'India',
  },
  {
    url: 'http://www.espncricinfo.com/team/_/id/25/bangladesh/',
    name: 'Bangladesh',
  },
  {
    url: 'http://www.espncricinfo.com/team/_/id/3/south-africa/',
    name: 'South Africa',
  },
  {
    url: 'http://www.espncricinfo.com/team/_/id/5/new-zealand/',
    name: 'New Zealand',
  },
]


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
          // this.setState({teams: response.data.results});
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
