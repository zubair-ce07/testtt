import React, { Component } from 'react';
import { connect } from 'react-redux';
import _ from 'lodash';

import { fetchMovies } from '../actions/index';
import MovieItem from './movie_item';
import SearchBar from './search_bar';


class MoviesIndex extends Component {
    componentWillMount() {
        this.props.fetchMovies('');
    }

    renderMovies() {
        return _.map(this.props.movies, movie => {
          return <MovieItem movie={movie} key={movie.id}/>;
        });
    }

    render() {
        return (
            <div>
              <h1 className="page-title">Movies</h1>
              <div className="row top-element">
                <div className="col-md-2"/>
                <div className="col-md-8">
                  <SearchBar onSearchTermChange={(term) => {this.props.fetchMovies(term);}}/>
                </div>
              </div><br/>
              <div className="row">
                <div className="col-md-2"/>
                <div className="col-md-8">
                  {this.renderMovies()}
                </div>
              </div>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {movies: state.movies};
}

export default connect(mapStateToProps, { fetchMovies })(MoviesIndex);
