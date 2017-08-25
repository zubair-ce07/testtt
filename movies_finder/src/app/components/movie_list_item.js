import React, {Component} from 'react';

class MovieListItem extends Component {
    render() {
        const {movie, onMovieSelect} = this.props;
        const imageUrl = getImageUrl(movie.poster_path, 'w92');

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
    }
}

export const getImageUrl = (path, size) => {
    return path ? `http://image.tmdb.org/t/p/${size}${path}` : '/images/no-img.png';
};

export default MovieListItem;
