import _ from 'lodash';
import React from 'react';
import MetaMovie from './meta_movie_item';


export const MovieList = ({movies, addToWatchlist, removeFromWatchlist}) => {
    return <div>{renderMovies(movies, addToWatchlist, removeFromWatchlist)}</div>
};

const renderMovies = (movies, addToWatchlist, removeFromWatchlist) => {
    return _.map(movies, movie => {
        return (
            <div className="mt-4" key={movie.id}>
                <MetaMovie movie={movie} addToWatchlist={addToWatchlist} removeFromWatchlist={removeFromWatchlist}/>
            </div>
        );
    });
};
