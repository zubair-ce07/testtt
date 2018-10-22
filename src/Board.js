import React from 'react';
import Square from './Square';

var Board = function(props){
  let count=0;
  function renderSquare(index) {
    return (
      <Square key={index}
        value={props.squares[index]}
        onClick={() => props.onClick(index)}
      />
    );
  }

  function renderRow(){
    let arr=[];
    for(let j=0;j < 3 ;j++)
    {
      arr.push(renderSquare(count));
      count++;
    }
    return arr;
  }

  function renderTable(){
    let arr=[];
    for(let i=0;i < 3 ;i++)
    {
      arr.push(<div className="board-row">{renderRow()}</div>);
    }

    return arr;
  }

    return (<div>{renderTable()}</div>);
}

export default Board;
