import React from 'react';
import {UncontrolledTooltip} from "reactstrap";

import {getImageUrl} from "../utils/utils";

const ActorItem = ({role, bestActor, onVotedActor}) => {
    const imageUrl = getImageUrl(role.person.profile, 'w138_and_h175_bestv2');
    return (
        <div className="actor-card">
            <img className="actor-img" src={imageUrl}/>
            <p className="votes-counter">{role.votes} {role.votes > 1 ? 'votes' : 'vote'}
                <i id={`${role.id}-actor`} onClick={() => onVotedActor(role.id)}
                   className={`fa ${bestActor !== role.id ? 'fa-thumbs-up' : 'fa-check-circle'} vote`}/></p>
            <UncontrolledTooltip
                target={`${role.id}-actor`}>{bestActor !== role.id ? 'Vote for actor' : 'Voted'}</UncontrolledTooltip>
            <p className="actor-name"><b>{role.person.name}</b></p>
            <p className="actor-character">{role.character}</p>
        </div>
    );
};

export default ActorItem;
