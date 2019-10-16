import React, { Component } from "react";
import  API  from "../api";

export class Program extends Component {
  state = { programs: [] };

  componentDidMount() {
    const id = this.props.match.params.id
    API.get(`institutions/${id}/programs/`).then(res => {
      const programs = res.data;
      this.setState({ programs });
    });
  }
  navigateToCourses(id){
    this.props.history.push(`/programs/${id}/courses/`)
  }
  renderPrograms = () => (
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
              {this.state.programs.map(program => (
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
                  <td>
                    <span>{program.campus.name}</span>
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
  )

  render() {
   return this.renderPrograms()
  }
}
