import React from "react";

export const CourseRow = ({ course}) => (
  <React.Fragment key={course.id}>
    <tr>
      <td>
        <span>{course.code}</span>
      </td>
      <td>
        <span>{course.name}</span>
      </td>
      <td>
        <span>{course.credit_hour}</span>
      </td>
    </tr>
  </React.Fragment>
);
