import React, { Component } from "react";
import axios from "axios";
import { EndPoint } from "../config";

export class Program extends Component {
  state = { Programs: [] };

  componentDidMount() {
    axios.get(EndPoint.programs).then(res => {
      const Programs = res.data;
      this.setState({ Programs });
    });
  }
  navigateToCourses(id){
    this.props.history.push(`/programs/${id}/courses/`)
  }

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-12">
            <div className="table-responsive">
              <table className="table  table-bordered table-condensed table-hover table-striped">
                <thead>
                  <tr>
                    <th scope="col">Programs</th>
                    <th scope="col">Branches</th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.Programs.map(program => (
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
                        <span onClick={(id) => this.navigateToCourses(program.id)} >{program.name}</span>
                      </td>
                    </tr>
                    </React.Fragment>  
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
