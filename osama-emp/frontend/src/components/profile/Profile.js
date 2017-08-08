import React from "react";
import "./Profile";

class Profile extends React.Component {
  constructor(props) {
    super();
  }

  render() {
    return (
      <p>
        Name:{" "}
        {this.props.profile.first_name + " " + this.props.profile.last_name}
      </p>
    );
  }
}

export default Profile;
