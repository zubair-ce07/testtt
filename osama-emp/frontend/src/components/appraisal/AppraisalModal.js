import React from "react";
import "./AppraisalModal.css";
import djangoapi from "../../djangoapi";

class AppraisalModal extends React.Component {
  submitAppraisal = evt => {
    evt.preventDefault();
    djangoapi.submitAppraisal(
      this.props.employee,
      evt.target.elements,
      jsonData => {
        console.log(jsonData);
      }
    );
    this.props.closeModal();
  };

  render() {
    return (
      <div className="modal-container">
        <div className="modal">
          <h3>
            Praise {this.props.employee}
          </h3>
          <form
            onSubmit={evt => {
              this.submitAppraisal(evt);
            }}
          >
            <label htmlFor="year">Year</label>
            <input
              name="year"
              type="number"
              min="2007"
              max={new Date().getFullYear()}
              placeholder="2007"
            />

            <label htmlFor="description">Description </label>
            <textarea type="text" name="description" />

            <label htmlFor="rating">Rating</label>
            <input
              name="rating"
              type="number"
              min="1"
              max="5"
              placeholder="5"
            />

            <button type="submit">Submit</button>

            <button onClick={() => this.props.closeModal()}>close</button>
          </form>
        </div>
      </div>
    );
  }
}

export default AppraisalModal;
