import React from 'react'
import Moment from 'moment';

import MetaMovie from './meta_movie_item';
import {getImageUrl} from '../utils/utils';
import {UncontrolledTooltip} from "reactstrap";
import {Link} from "react-router-dom";


const Activity = ({activity, addToWatchlist, removeFromWatchlist}) => {
    const {user, actions} = activity;
    return (
        <div className="card mt-4 border-0">
            <h3 className="card-header bd-1">
                <img className="rounded-circle img-profile"
                     src={user.photo === null ? '/images/avatar.jpg' : user.photo}/>
                <Link to="#"> {user.first_name} {user.last_name}</Link>
                <div className="float-right">
                    {renderAction('fa-plus-square', activity.id, actions.added_at, 'Added')}
                    {renderAction('fa-eye', activity.id, actions.watched_at, 'Watched')}
                    {renderAction('fa-reply', activity.id, actions.recommended_at, 'Recommended')}
                    {activity.rating === 'Liked' &&
                    renderAction('fa-thumbs-up', activity.id, actions.rated_at, 'Liked')}
                    {activity.rating === 'Disliked' &&
                    renderAction('fa-thumbs-down', activity.id, actions.rated_at, 'Disliked')}
                </div>
            </h3>
            {actions.voted_actor_at !== 0 &&
            <p className="card-header bd-1 padding-x6">
                {renderAction('fa-caret-up icon-voted', activity.id, actions.voted_actor_at, 'Voted')}
                <i id={"actor_photo" + activity.id}> {activity.best_actor.person.name}</i>
                {` as ${activity.best_actor.character}`}
                <UncontrolledTooltip placement="top" target={"actor_photo" + activity.id}>
                    <img src={getImageUrl(activity.best_actor.person.profile, 'w92')}/>
                </UncontrolledTooltip>
            </p>
            }
            <div className="card-block p-0">
                <MetaMovie movie={activity.movie} addToWatchlist={addToWatchlist}
                           removeFromWatchlist={removeFromWatchlist}/>
            </div>
        </div>
    );
};

const renderAction = (icon_class, activity_id, date_time, action) => {
    if (date_time === 0) return;
    return (
        <i id={action + activity_id} className={`fa ${icon_class} px-2`}>
            <UncontrolledTooltip placement="top" target={action + activity_id}>
                {`${action} ${Moment(date_time).calendar()}`}
            </UncontrolledTooltip>
        </i>
    );
};

export default Activity;
