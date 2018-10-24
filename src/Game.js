import React from 'react';
import {Square} from './Square';
import {Board} from './Board';
import calculateWinner from './Helper';

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      history: [{
        squares: Array(9).fill(null)
      }],
      stepNumber: 0,
      xIsNext: true
    };
  }

  handleClick(i) {
    let {
      'history': history,
      'stepNumber': stepNumber,
      'xIsNext': xIsNext
    } = this.state
    history = history.slice(0, stepNumber + 1);
    const current = history[history.length - 1];
    const squares = current.squares.slice();
    if (calculateWinner(squares) || squares[i]) {
      return;
    }
    squares[i] = xIsNext ? 'X' : 'O';
    this.setState({
      history: history.concat([{
        squares: squares
      }]),
      stepNumber: history.length,
      xIsNext: !xIsNext,
    });
  }

  jumpTo(step) {
    this.setState({
      stepNumber: step,
      xIsNext: (step % 2) === 0,
    });
  }

  getStatus(){
    let {
      'history': history,
      'stepNumber': stepNumber,
      'xIsNext': xIsNext
    } = this.state
    const current = history[stepNumber];
    const winner = calculateWinner(current.squares);

    let status;
    if (winner) {
      status = `Winner: ${winner}`;
    } else {
      status = `Next player: ${(xIsNext ? 'X' : 'O')}`;
    }
    return status;
  }

  getMoves(){
    const {'history': history} = this.state
    const moves = history.map((step, move) => {
      const desc = move ? `Go to move # ${move}` : 'Go to game start';
      return (<li key={move}>
                <button onClick={() => this.jumpTo(move)}>{desc}</button>
              </li>);
    });
    return moves;
  }

  render() {
    const {'history': history, 'stepNumber': stepNumber} = this.state
    const current = history[stepNumber];

    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares={current.squares}
            onClick={(i) => this.handleClick(i)}
          />
        </div>
        <div className="game-info">
          <div>{this.getStatus()}</div>
          <ol>{this.getMoves()}</ol>
        </div>
      </div>
    );
  }
}

export {Game};
