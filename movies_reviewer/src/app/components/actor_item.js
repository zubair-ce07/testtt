import React from 'react';
import {Link} from 'react-router-dom';

import {getImageUrl} from './movie_detail';

const ActorItem = ({person}) => {
    const imageUrl = getImageUrl(person.profile_path, 'w185');
    return (
        <div className="masonry-item text-center">
            <img width="100" src={imageUrl}/>
            <hr/>
            <Link to={`/actors/${person.id}`}><h4>{person.name}</h4></Link>
            <h5>As <b>{person.character}</b></h5>
        </div>
    );
};

export default ActorItem;
