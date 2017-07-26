import React from "react";
import { connect } from "react-redux";
import { playVideo } from "../actions";
import Result from "../components/Result";

class ResultContainer extends React.Component {
  render() {
    if (this.props.results.length > 0)
      return (
        <div className="result-container">
          {this.props.results.map(item =>
            <Result
              key={item.etag}
              imgurl={item.snippet.thumbnails.medium.url}
              title={item.snippet.title}
              description={item.snippet.description}
              vidId={item.id.videoId}
              playFunction={() => {
                this.props.onResultClick(item.id.videoId);
              }}
            />
          )}
        </div>
      );
    else {
      return <h1>Sorry, There are no results to display</h1>;
    }
  }
}

function mapDispatchToProps(dispatch) {
  return {
    onResultClick: vidId => {
      dispatch(playVideo(vidId));
    }
  };
}

function mapStateToProps(state) {
  return {
    results: state.results
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(ResultContainer);
