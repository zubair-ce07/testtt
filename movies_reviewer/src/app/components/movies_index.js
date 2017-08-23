import React, { Component } from 'react';
import { connect } from 'react-redux';
import _ from 'lodash';
import { Link } from 'react-router-dom';

import { fetchMovies } from '../actions/index'


class MoviesIndex extends Component {
    componentWillMount() {
        this.props.fetchMovies();
    }

    renderMovies() {
        return _.map(this.props.movies, movie => {
            let imageUrl = 'images/no-img.png';
            if (movie.poster_path)
                imageUrl = `http://image.tmdb.org/t/p/w92${movie.poster_path}`;

            return (
                <Link to={"/movies/" + movie.id}  key={movie.id}>
                  <div className="media item">
                    <img className="d-flex align-self-center mr-3" src={imageUrl}/>
                      <div className="media-body">
                        <h4 className="mt-0">{movie.title}</h4>
                        <h6>{movie.release_date}</h6>
                        <p>{movie.overview.substr(0, 250)}...</p>
                      </div>
                  </div>
                </Link>
            );
        });
    }

    render() {
        return (
            <div>
              <h1 className="page-title">Now Playing Movies</h1>
              <div className="center-aligned">
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
