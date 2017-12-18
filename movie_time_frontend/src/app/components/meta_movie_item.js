import _ from 'lodash';
import React, {Component} from 'react';
import {Link} from 'react-router-dom';

import {getImageUrl, cutString} from '../utils/utils';
import {Counters} from "./counters";


class MetaMovie extends Component {

    renderGenres() {
        return _.map(this.props.movie.genres, genre => {
            return <Link className="mr-1 ml-1" to={`/genres/${genre.id}/movies/`} key={genre.id}>{genre.name}</Link>
        })
    }

    render() {
        const {movie} = this.props;
        const imageUrl = getImageUrl(movie.max_voted_images.poster, 'w342');
        let action_btn = <button className="float-right fa fa-plus btn btn-success add-btn"
                                 onClick={() => this.props.addToWatchlist(movie.id)}/>;
        if (movie.user_statuses !== null && movie.user_statuses.removed === false)
            action_btn = <button className="float-right fa fa-remove btn btn-secondary add-btn"
                                 onClick={() => this.props.removeFromWatchlist(movie.id)}/>;

        return (
            <div className="row mx-0">
                <div className="col-md-3 p-0">
                    <img className="meta-poster" src={imageUrl}/>
                </div>
                <div className="col-md-9 movie-meta-data">
                    <h3 className="mt-2"><Link to={`/movies/${movie.id}/`}>{movie.title}</Link>
                        {action_btn}
                    </h3>
                    <h6><i className="fa fa-calendar"/> {movie.release_date}</h6>
                    <h6><i className="fa fa-hashtag"/> {this.renderGenres()}</h6>
                    <Counters movie={movie}/>
                    <p className="mb-0 text-justify">{cutString(movie.overview, 180)}</p>
                </div>
            </div>
        );
    }
}

export default MetaMovie;
