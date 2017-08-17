import React from 'react';
import './Mem.css';

export default function Memory(props){
        return (
            <div className="w3-container Main-memory-div">
              <div className="w3-card-4" >
                <header className="w3-container w3-blue">
                  <h3>{props.mem.title}</h3>
                </header>

                <div className="w3-container">
                  <p>{props.mem.text}</p>
                </div>

                <footer className="w3-container w3-blue">
                    <h6>{props.mem.tags}</h6>
                  <a href={props.mem.url}>Go to the link</a>
                </footer>
              </div>
            </div>
        );
}
