import React from 'react';
import { Link } from 'react-router-dom';

import {getImageUrl} from './movie_detail';

const MovieItem = ({movie}) => {
    const imageUrl = getImageUrl(movie.poster_path, 'w92');

	return (
      <Link to={"/movies/" + movie.id}>
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
};

export default MovieItem;
