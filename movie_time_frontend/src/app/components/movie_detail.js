import _ from 'lodash';
import {connect} from 'react-redux';
import React, {Component} from 'react';
import {Link} from 'react-router-dom';

import {voteActor} from '../actions/watchlist_actions';
import ActionPanel from './action_panel';
import {fetchingMovie, fetchMovieDetail} from '../actions/movies_actions';
import {getImageUrl, nFormatter} from "../utils/utils";
import {Counters} from "./counters";
import {UncontrolledTooltip} from "reactstrap";
import ActorItem from './actor_item';


class MovieDetail extends Component {
    componentWillMount() {
        this.props.fetchingMovie();
        this.props.fetchMovieDetail(this.props.match.params.movie_id);
    }

    renderGenres() {
        return _.map(this.props.movie_detail.movie.genres, genre => {
            return <Link className="mr-1 ml-1" to={`/genres/${genre.id}/movies/`} key={genre.id}>{genre.name}</Link>
        })
    }

    render() {
        const {movie_detail} = this.props;
        const {movie} = this.props.movie_detail;
        let divBg = null;
        if (!movie_detail.isFetching) {
            const imageUrl = getImageUrl(movie.max_voted_images.backdrop, 'w780');
            divBg = {
                background: `linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), url(\"${imageUrl}\") top left / cover`
            };
        }

        return (
            <div className="page-content mt-5">
                {movie_detail.isFetching && <h3>Loading...</h3>}
                {!movie_detail.isFetching &&
                <div className="mx-5">
                    <div style={divBg} className="border-radius-8">
                        <div className="row mx-0">
                            <div className="col-md-3 p-0">
                                <img className="float-right" height={400}
                                     src={getImageUrl(movie.max_voted_images.poster, 'w342')}/>
                            </div>
                            <div className="col-md-8 movie-detail-card my-auto">
                                <h1 className="mt-2 mb-3"><a href={movie.homepage}>{movie.title}</a></h1>
                                <h6 className="mb-0"><i className="fa fa-hashtag"/> {this.renderGenres()}</h6>
                                {this.renderMeta()}
                                <h5 className="text-center mt-3">{movie.tag_line}</h5>
                                <Counters movie={movie}/>
                                <p className="mb-0 text-justify mt-3">{movie.overview}</p>
                            </div>
                            <div className="col-md-1 p-0 my-auto">
                                <ActionPanel movie_id={movie.id} user_statuses={movie.user_statuses}/>
                            </div>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-2">
                            <h3 className="mt-5 mb-3">Top Actor</h3>
                            <div className="mb-5">{this.renderTopActor()}</div>
                        </div>
                        <div className="col-md-10">
                            <h3 className="mt-5 mb-3">Cast</h3>
                            <div className="horizontal-scroll mb-5">{this.renderCast()}</div>
                        </div>
                    </div>
                    <h3>Videos</h3>
                    <div className="mb-5 row videos-pane">{this.renderVideos()}</div>
                    <h3 className="mt-5 mb-3">Images</h3>
                    <div className="horizontal-scroll mb-5">{this.renderImages()}</div>
                </div>
                }
            </div>
        );
    }

    renderVideos() {
        const {videos} = this.props.movie_detail.movie;
        return _.map(videos, (video, index) => {
            return <div key={video.key} className="col-md-6 mt-3">
                <iframe className={index % 2 === 0 ? 'float-right' : ''} width="480" height="270"
                        src={`https://www.youtube.com/embed/${video.key}`} allowFullScreen={true}/>
            </div>
        });
    }

    renderImages() {
        const {images} = this.props.movie_detail.movie;
        return _.map(images, image => {
            return <a key={image.file_path} href={getImageUrl(image.file_path, 'original')}>
                <img src={getImageUrl(image.file_path, 'w342')} height={252}/>
            </a>;
        });
    }

    renderTopActor(){
        const {cast} = this.props.movie_detail.movie;
        const top = cast.slice().sort((a, b) => {return b.votes - a.votes})[0];
        if(top.votes === 0) return <h4>No data available. Be the first to vote</h4>;
        return <div><img src={getImageUrl(top.person.profile, 'w185')} width="100%"/>
            <p className="votes-counter">{top.votes} {top.votes > 1 ? 'votes' : 'vote'}</p></div>
    }

    renderCast() {
        const {cast} = this.props.movie_detail.movie;

        let bestActor = 0;
        if(this.props.movie_detail.movie.user_statuses !== null)
            bestActor = this.props.movie_detail.movie.user_statuses.best_actor;

        return _.map(cast, role => {
            return <ActorItem role={role} key={role.id} bestActor={bestActor}
                              onVotedActor={(role_id) => this.props.voteActor(role_id)}/>;
        });
    }

    renderMeta() {
        const {movie} = this.props.movie_detail;
        return <h6>
            <i className="fa fa-calendar counters"> {movie.release_date}</i>
            <i className="fa fa-cog counters"> {movie.status}</i>
            <i className="fa fa-clock-o counters" id="runtime"> {movie.runtime} Minutes</i>
            <UncontrolledTooltip placement="top" target={"runtime"}>Runtime</UncontrolledTooltip>
            <i className="fa fa-dollar counters" id="budget"> {nFormatter(movie.budget, 3)}</i>
            <UncontrolledTooltip placement="top" target={"budget"}>Budget</UncontrolledTooltip>
            <i className="fa fa-dollar counters" id="revenue"> {nFormatter(movie.revenue, 3)}</i>
            <UncontrolledTooltip placement="top" target={"revenue"}>Revenue</UncontrolledTooltip>
        </h6>;
    }
}


function mapStateToProps({movie_detail}, ownProps) {
    if (movie_detail.movie === null || movie_detail.movie.id.toString() !== ownProps.match.params.movie_id)
        movie_detail.isFetching = true;

    return {movie_detail};
}

export default connect(mapStateToProps, {fetchMovieDetail, fetchingMovie, voteActor})(MovieDetail);
