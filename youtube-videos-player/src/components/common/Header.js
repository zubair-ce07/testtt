import React, { Component } from 'react';
import PropTypes from 'prop-types';

class Header extends Component {
    // Header component
    static propTypes = {
        searchOnYoutube: PropTypes.func.isRequired,
    };

    render() {

        const searchOnYoutube = this.props.searchOnYoutube;

        return (
            <div className="header">
                <div className="search-bar">
                    <div className="youtube-logo">Youtube</div>
                    <div className="header-input-wrapper">
                        <input
                            type="text"
                            placeholder="Search on Youtube"
                            onChange={event => searchOnYoutube(event.target.value)}
                        />
                    </div>
                </div>
            </div>
        )
    }
}

export default Header
