import React from "react";

export const CourseTableBody = data => {
  return (
    <React.Fragment>
      <tr>
        <td colSpan={6}>
          <h5>
            <strong>Semester {data.number}</strong>
          </h5>
        </td>
      </tr>
      {data.semester_courses.map(course => (
        <tr key={course.id}>
          <td>{course.code}</td>
          <td>{course.name}</td>
          <td>{course.credit_hour}</td>
        </tr>
      ))}
    </React.Fragment>
  );
};
