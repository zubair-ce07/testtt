import React from 'react';


const MovieListItem = ({movie, onMovieSelect}) => {

    let imageUrl = 'images/no-img.png';
    if (movie.poster_path)
        imageUrl = `http://image.tmdb.org/t/p/w92${movie.poster_path}`;

    return (
        <li onClick={() => onMovieSelect(movie)} className="list-group-item">
            <div className="media">
                <img className="d-flex align-self-center mr-3" src={imageUrl}/>
                <div className="media-body">
                    <div className="media-heading">{movie.title}</div>
                </div>
            </div>
        </li>
    );
};

export default MovieListItem;
