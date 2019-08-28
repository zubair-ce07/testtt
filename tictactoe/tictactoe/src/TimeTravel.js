import React from "react";


class TimeTravel extends React.Component {
    jumpTo(step) {
        this.props.setState({
            stepNumber: step,
            xIsNext: step % 2 === 0
        });
    }

    render() {
        const current = this.props.history[this.props.stepNumber];
        const winner = this.props.calculateWinner(current.squares);
        let status;

        const moves = this.props.history.map((step, move) => {
            const desc = move ? "Go to move #" + move : "Go to game start";
            return (
                <li key={move}>
                    <button onClick={() => this.jumpTo(move)}>{desc}</button>
                </li>
            );
        });

        if (!winner)
            status = "Next player: " + (this.props.xIsNext ? "X" : "O");
        else
            status = "Winner: " + winner;

        return (
            <div>
                <div>{status}</div>
                <div>{moves}</div>
            </div>
        );
    }
}

export default TimeTravel;