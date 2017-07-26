import React from "react";
import PropTypes from "prop-types";
import "./Result.css";

class Result extends React.Component {
  render() {
    if (this.props.results.length > 0)
      return (
        <div className="result-container">
          {this.props.results.map(item =>
            <div
              key={item.etag}
              className="result"
              onClick={() => this.props.onResultClick(item.id.videoId)}
            >
              <img
                className="thumbnail"
                src={item.snippet.thumbnails.medium.url}
                alt={item.snippet.title}
              />
              <div className="detail">
                <h3 className="title">
                  {item.snippet.title}
                </h3>
                <p className="description">
                  {item.snippet.description}
                </p>
              </div>
            </div>
          )}
        </div>
      );
    else {
      return null;
    }
  }
}

Result.PropTypes = {
  imgurl: PropTypes.string,
  title: PropTypes.string,
  description: PropTypes.string
};

export default Result;
