import React from 'react';

import {getImageUrl, cutString} from '../../utils/utils';
import {Link} from "react-router-dom";
import {UncontrolledTooltip} from "reactstrap";


const Notification = ({notification, onDelete}) => {
    const movie = notification.action_object;
    const imageUrl = getImageUrl(movie.max_voted_images.poster, 'w154');
    return (
        <div className="notification-item row">
            <div className="col-md-2 p-0">
                <img src={imageUrl} height={70}/>
            </div>
            <div className="col-md-10">
                <h6><Link id={'movie' + movie.id} to={`/movies/${movie.id}/`}>{cutString(movie.title, 22, true)}</Link>
                    <i className="fa fa-close float-right delete-btn" onClick={() => onDelete(notification.id)}/></h6>
                {movie.release_date}<br/>
                <p className="float-right font-14 mb-0">Movie Released</p>
                <UncontrolledTooltip placement="bottom" target={'movie' + movie.id}>
                    {movie.title}
                </UncontrolledTooltip>
            </div>
        </div>
    );
};

export default Notification;
