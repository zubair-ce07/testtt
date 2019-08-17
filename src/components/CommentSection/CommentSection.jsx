import React, { Component } from "react";
import { connect } from "react-redux";
import AddComment from "./AddComment";
import CommentList from "./CommentList";

import "./CommentSection.css";

class CommentSection extends Component {
  state = { showComments: false, description: "View comments" };

  toggleComments = () => {
    this.setState({
      showComments: !this.state.showComments,
      description: this.state.showComments ? "View comments" : "Hide comments"
    });
  };

  renderComments = () => {
    if (this.state.showComments)
      return <CommentList postId={this.props.postId} />;
  };

  render = () => {
    return (
      <>
        <div>
          <div className="row no-gutters">
            <div className="col-10">
              <AddComment postId={this.props.postId} />
            </div>
            <button
              className="col-2 btn btn-light"
              onClick={this.toggleComments}
            >
              {this.state.description}
            </button>
          </div>
        </div>
        {this.renderComments()}
      </>
    );
  };
}

export default connect()(CommentSection);
