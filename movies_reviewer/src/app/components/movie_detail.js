import React, {Component} from 'react';
import {connect} from 'react-redux';
import {fetchMovie} from '../actions/index';
import {Link} from 'react-router-dom';

import Video from './video'

class MovieDetail extends Component {
    componentWillMount() {
        const {id} = this.props.match.params;
        this.props.fetchMovie(id);
    }

    render() {
        const {movie} = this.props;

        if (!movie) {
            return <div>Loading...</div>;
        }
        console.log(movie);
        let tube_key = null;
        if(movie.videos)
            tube_key = movie.videos.results[0].key;
        return (
            <div>
                <h1 className="page-title">{movie.title}</h1>
                <Link to="/">Back To Index</Link>
                <div className="center-aligned">
                    <Video videos={movie.videos}/>
                </div>
            </div>
        );
    }
}

function mapStateToProps(state, ownProps) {
    const requested_id = ownProps.match.params.id;

    if(!state.detailed_movie) {
        return {movie: state.movies[requested_id]};
    }
    const movie = state.detailed_movie.id === Number(requested_id)? state.detailed_movie: state.movies[requested_id];
    return {movie: movie};
}

export default connect(mapStateToProps, {fetchMovie})(MovieDetail)
