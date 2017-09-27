import React from 'react';


function VideoListItem(props){
    const video = props.video;
    const imageUrl = video.snippet.thumbnails.default.url;
    return (
        <li>
            <div>
                <div>
                    <div>
                        {video.snippet.title}
                    </div>
                </div>
                <div>
                    <img alt={ video.snippet.title } src={ imageUrl }  onClick={() => props.onSelect(video)}/>
                </div>
            </div>
        </li>
    );
}

function VideoList(props){
    const Items = props.videos.map((video) => {
        return (
            <VideoListItem
                onSelect={props.onSelect}
                key={ video.id.videoId }
                video={ video } />
        );
    });

    return (
        <ul>
            {Items}
        </ul>
    );

}

function VideoDetail(props){
    const video = props.video;
    if (!video) {
        return null;
    }
    const videoId = video.id.videoId;
    const video_url = "https://www.youtube.com/embed/" + videoId;

    return (
        <div>
            <div>
                <iframe src={ video_url } title={ video.snippet.title }></iframe>
            </div>
            <div>
                <div>
                    { video.snippet.title }
                </div>
                <div>
                    { video.snippet.description }
                </div>
                <div>
                    { video.snippet.publishedAt }
                </div>

            </div>
        </div>
    );
}

export { VideoDetail };
export { VideoList };
export { VideoListItem };


