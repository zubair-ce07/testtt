import {connect} from 'react-redux';
import React, {Component} from 'react';

import {updateWatchlist, rateMovie, removeFromWatchlist, addToWatchlist} from "../actions/watchlist_actions";
import {UncontrolledTooltip} from "reactstrap";


class ActionPanel extends Component {
    updateWatchlist(action) {
        const {movie_id} = this.props;
        const stats = this.props.user_statuses;
        if (action === 'watched' && !isAdded(stats)) return;
        if (action === 'recommended' && !isWatched(stats)) return;
        let type = 'PUT';
        if (action === 'watched' && isWatched(stats)) type = 'DELETE';
        if (action === 'recommended' && isRecommended(stats)) type = 'DELETE';
        this.props.updateWatchlist(movie_id, action, type);
    }

    rateMovie(rating) {
        const {movie_id} = this.props;
        const stats = this.props.user_statuses;
        if (!isWatched(stats)) return;
        let type = 'PUT';
        if (isRated(rating, stats)) type = 'DELETE';
        this.props.rateMovie(movie_id, rating, type);
    }

    render() {
        const {movie_id} = this.props;
        const stats = this.props.user_statuses;
        return <div className="float-right actions-wrapper">
            <div onClick={() => {
                isAdded(stats) ? this.props.removeFromWatchlist(movie_id) : this.props.addToWatchlist(movie_id)
            }}
                 className={`action-btn ${isAdded(stats) ? 'active-action' : ''}`} id={`${movie_id}-add`}>
                <i className="fa fa-plus-square"/>
            </div>
            <div onClick={() => this.updateWatchlist('watched')} id={`${movie_id}-watch`}
                 className={`action-btn ${isAdded(stats) ? '' : 'disabled-action'} ${isWatched(stats) ? 'active-action' : ''}`}>
                <i className="fa fa-eye"/>
            </div>
            <div onClick={() => this.updateWatchlist('recommended')} id={`${movie_id}-recommend`}
                 className={`action-btn ${isWatched(stats) ? '' : 'disabled-action'} ${isRecommended(stats) ? 'active-action' : ''}`}>
                <i className="fa fa-reply"/></div>
            <div onClick={() => this.rateMovie('Liked')} id={`${movie_id}-like`}
                 className={`action-btn ${isWatched(stats) ? '' : 'disabled-action'} ${isRated('Liked', stats) ? 'active-action' : ''}`}>
                <i className="fa fa-thumbs-up"/>
            </div>
            <div onClick={() => this.rateMovie('Disliked')} id={`${movie_id}-dislike`}
                 className={`action-btn ${isWatched(stats) ? '' : 'disabled-action'} ${isRated('Disliked', stats) ? 'active-action' : ''}`}>
                <i className="fa fa-thumbs-down"/>
            </div>
            <UncontrolledTooltip target={`${movie_id}-add`} placement="left">
                {isAdded(stats) ? 'Remove from watchlist' : 'Add to watchlist'}
            </UncontrolledTooltip>
            <UncontrolledTooltip target={`${movie_id}-watch`} placement="left">
                {!isAdded(stats) ? 'First Add this to watchlist'
                    : isWatched(stats) ? 'Mark as Unwatched' : 'Mark as Watched'}
            </UncontrolledTooltip>
            <UncontrolledTooltip target={`${movie_id}-recommend`} placement="left">
                {!isWatched(stats) ? 'Recommending before watching? eh...'
                    : isRecommended(stats) ? 'Remove Recommendation' : 'Recommend to Followers'}
            </UncontrolledTooltip>
            <UncontrolledTooltip target={`${movie_id}-like`} placement="left">
                {!isWatched(stats) ? 'Liking before watching? huh?'
                    : isRated('Liked', stats) ? 'Remove Like' : 'Add Like'}
            </UncontrolledTooltip>
            <UncontrolledTooltip target={`${movie_id}-dislike`} placement="left">
                {!isWatched(stats) ? 'Disliking before watching? huh?'
                    : isRated('Disliked', stats) ? 'Remove Dislike' : 'Add Dislike'}
            </UncontrolledTooltip>
        </div>;
    }
}

const isRated = (rating, statuses) => {
    return isWatched(statuses) && statuses.rating === rating
};
const isRecommended = statuses => {
    return isWatched(statuses) && statuses.is_recommended
};
const isAdded = statuses => {
    return statuses !== null && statuses.removed === false
};
const isWatched = statuses => {
    return isAdded(statuses) && statuses.is_watched
};


export default connect(null, {updateWatchlist, rateMovie, removeFromWatchlist, addToWatchlist})(ActionPanel);
