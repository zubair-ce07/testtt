import React from "react";
import "./Profile";

class Profile extends React.Component {
  constructor(props) {
    super();
  }

  render() {
    return (
      <div className="profile">
        <p>
          Username: {this.props.profile.username}
        </p>
        <p>
          Name:{" "}
          {this.props.profile.first_name + " " + this.props.profile.last_name}
        </p>
        <p>
          Job Title: {this.props.profile.job_title}
        </p>
        <p>
          Gender: {this.props.profile.gender === "M" ? "Male" : "Female"}
        </p>
        <p>
          Date of Birth: {this.props.profile.date_of_birth}
        </p>
        <p>
          Date of Joining: {this.props.profile.date_of_joining}
        </p>
        <p>
          Nationality: {this.props.profile.nationality}
        </p>
      </div>
    );
  }
}

export default Profile;
