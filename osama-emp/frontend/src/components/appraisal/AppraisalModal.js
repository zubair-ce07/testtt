import React from "react";
import "./AppraisalModal.css";

class AppraisalModal extends React.Component {
  render() {
    return (
      <div className="modal-container">
        <div className="modal">
          <form>
            <label htmlFor="year">Year</label>
            
            <input
              type="number"
              min="2007"
              max={new Date().getFullYear()}
              placeholder="2007"
            />

            <label htmlFor="description">Description </label>
            <input type="text" name="description" />
          </form>
        </div>
      </div>
    );
  }
}

export default AppraisalModal;
