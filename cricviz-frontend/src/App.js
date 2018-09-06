import React, { Component } from 'react';

import './App.css';
import NavBar from './components/nav_bar';
import ArticleListItem from './components/article_list_item';
import ArticleList from './components/article_list';

const ARTICLES = [
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
        <div>
          <NavBar />
          <ArticleList articles={this.state.articles}/>
        </div>
    );
  }
}

export default App;
