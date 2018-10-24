import React from 'react';
import PropTypes from 'prop-types';

let Square = function(props) {
  return (
    <button className="square" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

Square.propTypes={
  value:PropTypes.string
}



export {Square};
