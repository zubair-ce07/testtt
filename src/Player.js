import React, { Component } from 'react';
import './App.css';
import YouTube from 'react-yt';
import PropTypes from 'prop-types';


class Player extends Component {

    render() {
        return (
            <div style={{paddingLeft:50, paddingTop:50}} className={'pull-left'}>
                <YouTube videoId={this.props.match.params.id} autoplay={true}/>
            </div>
        );
    }
}

Player.propTypes = {
    match: PropTypes.shape({
        params: PropTypes.shape({
            id: PropTypes.string,
        }),
    }),
};
export default Player;