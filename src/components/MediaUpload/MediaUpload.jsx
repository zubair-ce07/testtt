import React, { Component } from "react";
import { connect } from "react-redux";

import "./MediaUpload.sass";

import uploadIcon from "./upload-icon.png";
import { removeMedia, addMedia } from "../../actions/media.action";

class MediaUpload extends Component {
  onChangeHandler = event => {
    this.props.addMedia(event.target.files[0]);
  };

  deleteUploadedImage = imageToDelete => {
    this.props.removeMedia(imageToDelete);
  };

  renderImages = () => {
    return this.props.media.map((file, i) => {
      return (
        <div className="image-preview" key={i}>
          <div
            className="delete-image"
            onClick={() => this.deleteUploadedImage(file)}
          >
            &times;
          </div>
          <img src={URL.createObjectURL(file)} alt="#" />
        </div>
      );
    });
  };

  renderSquareLabel = () => {
    if (this.props.media.length > 0)
      return (
        <label htmlFor="file-input">
          <div className="square-upload">
            <div className="plus-image">&#43;</div>
          </div>
        </label>
      );
    else return null;
  };

  renderLabel = () => {
    if (this.props.media.length === 0) {
      return (
        <label id="image-upload-label" htmlFor="file-input">
          <img className="upload-icon" src={uploadIcon} alt="#" />
          <span id="image-upload-label-text">Upload Photos</span>
        </label>
      );
    }
  };

  render = () => {
    return (
      <>
        <div className="images-to-upload">
          {this.renderImages()}
          {this.renderSquareLabel()}
        </div>
        <div className="image-upload">
          {this.renderLabel()}
          <input id="file-input" type="file" onChange={this.onChangeHandler} />
        </div>
      </>
    );
  };
}
const mapStateToProps = state => {
  return { media: state.media };
};

export default connect(
  mapStateToProps,
  { addMedia, removeMedia }
)(MediaUpload);
