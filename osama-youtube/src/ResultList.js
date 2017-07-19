import React from "react";
import Result from "./Result";

class ResultList extends React.Component {
  constructor(props) {
    super();
  }

  render() {
    return (
      <div>
        {this.props.list.map(item => {
          return (
            <Result
              key={item.etag}
              imgurl={item.snippet.thumbnails.medium.url}
              title={item.snippet.title}
              description={item.snippet.description}
              vidId={item.id.videoId}
              play={this.playVideo}
            />
          );
        })}
      </div>
    );
  }
}

export default ResultList;
