import React from 'react';


const Video = (props) => {
    if(!props.videos)
        return null;
    return(
        <iframe className="youtube" src={`https://www.youtube.com/embed/${props.videos.results[0].key}`}/>
    );
};

export default Video;
