import React, { Component } from "react";

import "./MediaUpload.sass";

import uploadIcon from "./upload-icon.png";

class MediaUpload extends Component {
  state = { media: [] };

  onChangeHandler = async event => {
    await this.setState({
      media: [...this.state.media, event.target.files[0]]
    });
    this.props.onMediaChange(this.state.media);
  };

  deleteUploadedImage = async imageToDelete => {
    await this.setState({
      media: this.state.media.filter(img => img !== imageToDelete)
    });
    this.props.onMediaChange(this.state.media);
  };

  renderImages = () => {
    return this.state.media.map((file, i) => {
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
    if (this.state.media.length > 0)
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
    if (this.state.media.length === 0) {
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

export default MediaUpload;
