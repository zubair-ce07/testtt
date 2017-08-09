import React from "react";
import "./Profile";
import djangoapi from "../../djangoapi";
import Appraisal from "../appraisal/Appraisal";

class Profile extends React.Component {
  constructor(props) {
    super();
    this.state = {
      appraisals: []
    };
  }

  componentDidMount() {
    djangoapi.getAppraisals(this.props.profile.username, jsonData => {
      this.setState({
        appraisals: jsonData.appraisals.sort((a, b) => b.year - a.year)
      });
    });
  }

  componentDidUpdate() {
    this.componentDidMount();
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
        <p>
          Reports To: {this.props.profile.reports_to}
        </p>
        <div className="appraisal-container">
          {this.state.appraisals !== []
            ? this.state.appraisals.map(current => {
                return <Appraisal key={current.year} data={current} />;
              })
            : null}
        </div>
      </div>
    );
  }
}

export default Profile;
