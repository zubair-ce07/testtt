import React, { Component } from 'react';

import ListItem from './recommented_list_item'

class VideosList extends Component{

    render(){
        const videoList = this.props.videosList.map(item => {
            return (
                <ListItem
                    key={item.etag}
                    video={item}
                    onVideoSelection={this.props.onVideoSelection}
                />
            );
        });
        return(
            <ul className="col-md-4 list-group">
                {videoList}
            </ul>
        );
    }//render

}//class

export default VideosList;
