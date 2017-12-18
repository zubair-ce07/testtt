import React from 'react';
import {getImageUrl} from './movie_list_item'

const MovieDetail = ({movie}) => {
    if (!movie) {
        return <div>Loading...</div>;
    }

    const imageUrl = getImageUrl(movie.poster_path, 'w500');
    const backdrop_url = getImageUrl(movie.backdrop_path, 'w780');

    return (
        <div className="movie-detail-container col-md-9 ">
            <div className="row">
                <div className="col-md-5">
                    <img className="img-thumbnail" width="450px" src={imageUrl}/>
                </div>
                <div className="col-md-6 movie-details">
                    <img className="backdrop img-fluid" src={backdrop_url}/>
                    <br/>
                    <h2><u>{movie.title}</u></h2><br/>
                    <h6><b>Release Date: </b>{movie.release_date}</h6>
                    <h6><b>Rating: </b>{movie.vote_average} <b>By: </b>{movie.vote_count} People</h6>
                    <p>{movie.overview}</p>
                </div>
            </div>
        </div>
    );
};

export default MovieDetail;
