import React, { Component } from 'react';
import { connect } from 'react-redux';
import { fetchCategoryNews } from '../actions'
import SearchBar from '../components/search_bar'
import NewsThumbnailList from '../components/news_thumbnail_list';


class NewsList extends Component {
    constructor(props) {
      super(props)
      this.state = {
        error:false
      }
    }

    componentDidMount(){
        const name = this.props.match.params.name;
        this.props.fetchCategoryNews(name).then(()=> {
          this.setState({ error: false })
        }).catch(() => {
          this.setState({error: true})
        })
    }

    renderNewsList() {
        if(this.state.error)
        {
            return(
                <h3>No News for {this.props.match.params.name}</h3>
            );
        }
        if (!this.props.newsList){

            return (
              <div>Loading...</div>
            );
        }
        return (
            <div>
                <NewsThumbnailList news_list={ this.props.newsList } />
            </div>
        );
    }

    render(){
      return(
        <div>
            <SearchBar />
            <h1>{this.props.match.params.name}</h1>
            {this.renderNewsList()}
        </div>
      );
    }
}

function mapStateToProps(state) {
    return {
        newsList: state.newsList,
    };
}


export default connect(mapStateToProps, { fetchCategoryNews })(NewsList);
