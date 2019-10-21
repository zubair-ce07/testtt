import React from "react";

import Table from "react-bootstrap/Table";

const renderCourseTableData = data => {
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

const renderProgramsTableData = (data, navigate) => {
  return data.map(program => (
    <React.Fragment>
      <tr>
        <td colSpan={6}>
          <h4>
            <strong>{program.category}</strong>
          </h4>
        </td>
      </tr>
      <tr>
        <td>
          <span onClick={id => navigate(program.id)}>{program.name}</span>
        </td>
        <td>
          <span>{program.campus.name}</span>
        </td>
      </tr>
    </React.Fragment>
  ));
};

export const AppTable = ({ headers, data, type, navigate }) => {
  return (
    <Table striped bordered hover variant="dark">
      <thead>
        <tr>
          {headers.map(header => (
            <th key={header.id}>{header.name}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {type === "course"
          ? renderCourseTableData(data, navigate)
          : renderProgramsTableData(data)}
      </tbody>
    </Table>
  );
};
