import React from 'react'
import './Auth.css'

function LoginLayout (Form) {
  class Component extends React.Component {
    render () {
      return (

        <div className="main">

          <section className="signup">
            <div className="container">
              <div className="signup-content">
                <Form {...this.props}></Form>
              </div>
            </div>
          </section>
        </div>
      )
    }
  }

  Component.displayName = 'LoginLayout'

  return Component
}

export default LoginLayout
