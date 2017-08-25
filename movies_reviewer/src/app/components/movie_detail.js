import {connect} from 'react-redux';
import React, {Component} from 'react';
import {Link} from 'react-router-dom';

import ActorItem from './actor_item';
import {fetchMovie} from '../actions/index';

class MovieDetail extends Component {
    componentWillMount() {
        this.props.fetchMovie(this.props.match.params.id);
    }

    static renderList(list) {
        return list.map(item => {
            return item.name + ', ';
        });
    }

    render() {
        const {movie} = this.props;
        if (!movie)
            return <h3 className="loading-indicator">Loading...</h3>;

        const imageUrl = getImageUrl(movie.backdrop_path, 'w780');
        const posterUrl = getImageUrl(movie.poster_path, 'w342');
        const divBg = {
            background: `linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), url(\"${imageUrl}\") top left / cover`
        };

        return (
            <div>
                <h1 className="page-title">{movie.title}</h1>
                <div style={divBg} className="movie-detail top-element">
                    <div className="row">
                        <div className="col-md-4 text-center">
                            <img src={posterUrl}/>
                        </div>
                        <div className="col-md-8 movie-meta">
                            <br/><h5 className="text-center">{movie.tagline}</h5>
                            <br/><h4>Overview</h4>
                            <p>{movie.overview}</p><br/>
                            <h6><b>Status: </b>{movie.status}</h6>
                            <h6><b>Rating: </b>{movie.vote_average}/10 By {movie.vote_count} People</h6>
                            <h6><b>Runtime: </b>{movie.runtime} Mins</h6>
                            <br/><h6><b>Budget: </b>{movie.budget}$</h6>
                            <h6><b>Genres: </b>{MovieDetail.renderList(movie.genres)}</h6>
                            <h6><b>Production Countries: </b>{MovieDetail.renderList(movie.production_countries)}</h6>
                            <h6><b>Production Companies: </b>{MovieDetail.renderList(movie.production_companies)}</h6>
                            <Link className="btn btn-primary" to={`/movies/${movie.id}/reviews`}>Add Review</Link>
                        </div>
                    </div>
                </div>
                <div className="masonry">
                    {this.renderCredits()}
                </div>
            </div>
        );
    }

    renderCredits() {
        return this.props.movie.credits.cast.map(person => {
            return <ActorItem person={person} key={person.credit_id}/>;
        });
    }
}

function mapStateToProps(state, ownProps) {
    const props = {movie: null};
    if (state.detailed_movie && state.detailed_movie.id === Number(ownProps.match.params.id))
        props["movie"] = state.detailed_movie;
    return props;
}


export const getImageUrl = (path, size) => {
    return path ? `http://image.tmdb.org/t/p/${size}${path}` : '/images/no-img.png';
};

export default connect(mapStateToProps, {fetchMovie})(MovieDetail);
