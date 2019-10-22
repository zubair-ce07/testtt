import React from "react";

export const ProgramTableBody = (data, navigate) => {
  console.log("navigate", navigate);
  return data.map(program => (
    <React.Fragment key={program.id}>
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
