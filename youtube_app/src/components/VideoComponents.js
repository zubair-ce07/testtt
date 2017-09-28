import React from 'react';


export function VideoListItem(props){
    const { video } = props;
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

export function VideoList(props){
    return (
        <ul>
            {props.videos.map((video) =>
                    <VideoListItem onSelect={props.onSelect} key={ video.id.videoId } video={ video } />
            )}
        </ul>
    );

}

export function VideoDetail(props){
    const { video } = props;
    const videoUrl = "https://www.youtube.com/embed/" + video.id.videoId;

    return (
        <div>
            <div>
                <iframe src={ videoUrl } title={ video.snippet.title }></iframe>
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



