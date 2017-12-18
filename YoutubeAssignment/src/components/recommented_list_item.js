import React, { Component } from 'react';

class ListItem extends Component{

    render(){
        const imageUrl = this.props.video.snippet.thumbnails.default.url;
        const title = this.props.video.snippet.title;

        return(
            <li onClick={() => this.props.onVideoSelection(this.props.video)} className="list-group-item">
                <div className="video-list media">
                    <div className="media-left">
                        <img className="media-object" src={imageUrl} />
                    </div>
                    <div className="media-body">
                        <div className="media-heading">{title}</div>
                    </div>
                </div>
            </li>
        );
    }//render

}//class

export default ListItem;
