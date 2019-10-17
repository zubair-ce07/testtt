import React from "react";

export const CourseHeaderRow = ({ semester }) => (
  <React.Fragment>
    <tr>
      <td colSpan={6}>
        <h5>
          <strong>Semester {semester.number}</strong>
        </h5>
      </td>
    </tr>
  </React.Fragment>
);
