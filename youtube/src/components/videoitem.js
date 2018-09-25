import React from 'react';

const VideoThumbnail = (props) =>
{
  const video = props.video,
        title = (video.snippet.title).substring(0, 50) + " ...",
        url = "https://www.youtube.com/embed/" + video.id.videoId;
  return(
    <div className="row ml-1">
      <div className={props.playerCheck ? "col-md-6" : "col-xs-6 ml-5"}>
        <img className="img-thumbnail thumbnail" alt={video.snippet.title} src={video.snippet.thumbnails.default.url} />
      </div>
        <div className="custom-column col-md-6">
          <a onClick={() => props.videoURL(url)} href="#" className="ml-2 mt-3">
            {title}
          </a>
          {props.playerCheck ?
            null
            :
            <div className="small ml-2">
              {video.snippet.description}
            </div>
          }
        </div>
    </div>
  )
};

export default VideoThumbnail;
