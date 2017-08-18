import React from 'react';

const MovieDetail = ({movie}) => {
    if (!movie) {
        return <div>Loading...</div>;
    }

    let imageUrl = 'images/no-img.png';
    let backdrop_url = 'images/no-img.png';
    if (movie.poster_path)
        imageUrl = `http://image.tmdb.org/t/p/w500${movie.poster_path}`;
    if (movie.backdrop_path)
        backdrop_url = `http://image.tmdb.org/t/p/w780${movie.backdrop_path}`;

    return (
        <div className="movie-detail col-md-9 ">
            <div className="row">
                <div className="col-md-5">
                    <img className="img-thumbnail" width="450px" src={imageUrl}/>
                </div>
                <div className="col-md-6 details">
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
