import React from 'react';
import ContentEditable from 'react-simple-contenteditable'
import PropTypes from 'prop-types'
export default class Service extends React.Component {
    static propTypes={
        id : PropTypes.number,
    }

    constructor(props) {
        super(props);
        this.id = props.id;
        this.state = {
            html:{heading: "",
                  description:""}
        }
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(event, value){
      console.log("change",value);
      const field = event.target.id;
      const html = this.state.html;
      html[field] = value;
      this.setState({
         html   
      });
       console.log("changed",this.state.html.heading);
    }

    render() {
        return (
                <div>
                    <div className="col-md-4 icon-service">
                       <div className="icon" >
                        <i className="fa fa-calendar"></i>
                       </div>
                       <div className="icon-box-body">
                            <div className="row">
                              <div>
                                  <div className="col-md-offset-1 col-md-8">
                                      <div className="col-md-10">
                                        <ContentEditable
                                          html={this.state.html.heading}
                                          tagName="h4"
                                          id="heading"
                                          onChange={ this.handleChange }
                                          contentEditable="plaintext-only"
                                        />
                                    </div>
                                  </div>
                              </div>
                            </div>
                            <div className="row">
                              <div>
                                  <div className="col-md-offset-1 col-md-8">
                                      <ContentEditable
                                          html={this.state.html.description}
                                          tagName="p"
                                          id="description"
                                          onChange={ this.handleChange }
                                          contentEditable="plaintext-only"
                                        />
                                  </div>
                              </div>
                            </div>
                        </div>
                    </div>
                </div>      
        );
    }
}
