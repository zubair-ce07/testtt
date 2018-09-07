import React, { Component } from 'react';

import './App.css';
import NavBar from './home/components/navBar';
import ArticleListItem from './home/components/articleListItem';
import ArticleList from './home/components/articleList';
import HeadlinesList from './home/components/headlinesList';
import { BrowserRouter as Router, Route, Link, NavLink } from "react-router-dom";

const ARTICLES = [
  {
    url: 'http://a2.espncdn.com/combiner/i?img=%2Fi%2Fcricket%2Fcricinfo%2F1134328_900x600.jpg&w=570',
    title: `Would have liked to take Virat Kohli's wicket - Hasan Ali`,
    description: 'The absence of Indian captain will give Pakistan the edge in the Asia Cup, said the fast bowler',
  },
  {
    url: 'http://a2.espncdn.com/combiner/i?img=%2Fi%2Fcricket%2Fcricinfo%2F1149080_1296x729.jpg&w=920&h=518&scale=crop&cquality=80&location=origin',
    title: 'Grant Bradburn appointed Pakistan fielding coach',
    description: 'The former NewZealand allrounder, will fill the void left by Steve Rixons departure',
  },
  {
    url: 'http://a4.espncdn.com/combiner/i?img=%2Fi%2Fcricket%2Fcricinfo%2F1140540_1296x729.jpg&w=920&h=518&scale=crop&cquality=80&location=origin',
    title: 'Confusion over Shakib al Hassans fitness for Asia Cup',
    description: 'Bangladesh captain and coach feel the allrounder is fit enough to play but Shakib disagrees',
  }

]

class App extends Component {
  constructor(props) {
    super(props);

    this.state = { articles: ARTICLES };

  }


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

              <ArticleList articles={this.state.articles}/>
              <HeadlinesList />
              
          </div>
        </Router>
    );
  }
}

const Home = () => (
  <div>
    <h2 >Home</h2>
    <h2>Home</h2>
    <h2>Home</h2>
    <h2>Home</h2>
  </div>
);

const LiveScores = () => (
  <div>
    <h2>Live Scores</h2>
  </div>
);

const PlayerInsights = () => (
  <div>
    <h2>Player Insights</h2>

  </div>
);

const FollowPlayers = () => (
  <div>
    <h2>Follow Players</h2>
  </div>
);

const FollowTeams = () => (
  <div>
    <h2>Follow Teams</h2>
  </div>
);

const TeamsHome = () => (
  <div>
    <h2>Teams Home</h2>
  </div>
);

export default App;
