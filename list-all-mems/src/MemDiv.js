import React from 'react';
import './Mem.css'


class MemDiv extends React.Component{
    render(){
        return (
            <div className="w3-container" style={{width:'50%', margin:'50px'}}>
              <div className="w3-card-4" >
                <header className="w3-container w3-blue">
                  <h3>{this.props.mem.title}</h3>
                </header>

                <div className="w3-container">
                  <p>{this.props.mem.text}</p>
                </div>

                <footer className="w3-container w3-blue">
                    <h6>{this.props.mem.tags}</h6>
                  <a href={this.props.mem.url}>Go to the link</a>
                </footer>
              </div>
            </div>
        );
    }
}

export default MemDiv;