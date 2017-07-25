import React from "react";

import { connect } from "react-redux";

import Result from "../components/Result";

class ResultContainer extends React.Component {
  // handleClick() {
  //   // this.props.play(this.props.vidId);
  // }
  render() {
    // return this.props.results.length !== 0
    // ? this.props.results.map(item =>
    if (this.props.results.length > 0)
      return (
        <div>
          {this.props.results.map(item =>
            <Result
              key={item.etag}
              imgurl={item.snippet.thumbnails.medium.url}
              title={item.snippet.title}
              description={item.snippet.description}
              vidId={item.id.videoId}
            />
          )}
        </div>
      );
    else {
      return <h1>Sorry, There are no results to display</h1>;
    }
    // )
  }
}

function mapStateToProps(state) {
  return {
    results: state.results
  };
}

export default connect(mapStateToProps)(ResultContainer);
