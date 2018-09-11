import './App.css';
import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import NavBar from './home/components/NavBar';
import Home from './home/components/Home';
import LiveScores from './scores/components/LiveScores';
import PlayerInsights from './players/components/PlayerInsights';
import FollowPlayers from './players/components/FollowPlayers';
import FollowTeams from './teams/components/FollowTeams';
import TeamsHome from './teams/components/TeamsHome';
import SearchBar from './home/containers/SearchBar';

class App extends Component {
  render() {
    return (
        <Router>
          <div>
            <NavBar />

              <Route exact path="/" component={Home} />
              <Route path="/live-scores" component={LiveScores} />
              <Route path="/player-insights" component={PlayerInsights} />
              <Route path="/follow-players" component={FollowPlayers} />
              <Route path="/follow-teams" component={FollowTeams} />
              <Route path="/teams-home" component={TeamsHome} />

          </div>
        </Router>
    );
  }
}

export default App;
