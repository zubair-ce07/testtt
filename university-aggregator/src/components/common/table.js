import React from "react";

import Table from "react-bootstrap/Table";
import { CourseTableBody } from "./CourseTableBody";
import { ProgramTableBody } from "./ProgramTableBody";

const tableBody = {
  course: CourseTableBody,
  programs: ProgramTableBody
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
      <tbody>{tableBody[type](data, navigate)}</tbody>
    </Table>
  );
};
