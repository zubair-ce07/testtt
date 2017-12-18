import React from 'react';

import MovieListItem from './movie_list_item';


const MovieList = (props) => {
    const movieItems = props.movies.map((movie) => {
        return <MovieListItem onMovieSelect={props.onMovieSelect} key={movie.id} movie={movie}/>;
    });

    return (
        <ul className="movie-list col-md-3 list-group">
            {movieItems}
        </ul>
    );
};

export default MovieList;
