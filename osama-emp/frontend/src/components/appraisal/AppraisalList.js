import React from "react";
import Appraisal from "./Appraisal";
import djangoapi from "../../djangoapi";

class AppraisalList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      appraisals: []
    };
  }

  componentWillReceiveProps(props) {
    djangoapi.getAppraisals(props.name, jsonData => {
      this.setState({
        appraisals: jsonData.appraisals.sort((a, b) => b.year - a.year)
      });
    });
  }

  render() {
    // console.log(this.props);
    return (
      <div>
        {this.state.appraisals !== []
          ? this.state.appraisals.map(current => {
              return <Appraisal key={current.year} data={current} />;
            })
          : null}
      </div>
    );
  }
}

export default AppraisalList;
