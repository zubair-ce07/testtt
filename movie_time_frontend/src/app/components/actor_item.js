import React from 'react';
import {UncontrolledTooltip} from "reactstrap";

import {getImageUrl, cutString} from "../utils/utils";

const ActorItem = ({role, bestActor, onVotedActor}) => {
    const imageUrl = getImageUrl(role.person.profile, 'w138_and_h175_bestv2');
    const personName = cutString(role.person.name, 17, true);
    const character = cutString(role.character, 25, true);
    return (
        <div className="actor-card">
            <img className="actor-img" src={imageUrl}/>
            <p className="votes-counter">{role.votes} {role.votes > 1 ? 'votes' : 'vote'}
                <i id={`${role.id}-actor`} onClick={() => {if(bestActor !== 0) onVotedActor(role.id)}}
                   className={`fa ${bestActor !== role.id ? 'fa-thumbs-up' : 'fa-check-circle'} vote`}/></p>
            <UncontrolledTooltip
                target={`${role.id}-actor`}>
                {bestActor === 0? 'Add Movie To Vote': bestActor !== role.id ? 'Vote for actor' : 'Voted'}
                </UncontrolledTooltip>
            <p className="actor-name" id={`actorName-${role.id}`}><b>{personName}</b></p>
            <p className="actor-character" id={`chracter-${role.id}`}>{character}</p>
            {personName !== role.person.name && <UncontrolledTooltip target={`actorName-${role.id}`}>{role.person.name}
            </UncontrolledTooltip>}
            {character !== role.character && <UncontrolledTooltip target={`chracter-${role.id}`}>{role.character}
            </UncontrolledTooltip>}
        </div>
    );
};

export default ActorItem;
