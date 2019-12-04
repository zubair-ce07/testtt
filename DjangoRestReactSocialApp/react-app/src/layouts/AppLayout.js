import React from 'react'
import AppHeader from '../components/App/AppHeader'

function AppLayout (Child) {
  class Component extends React.Component {
    render () {
      return (
        <>
          <AppHeader {...this.props}/>
          <Child {...this.props}/>
          {/* <AppFooter {...this.props}/> */}
        </>
      )
    }
  }

  Component.propTypes = {
    // route: React.PropTypes.object.isRequired,
  }

  Component.displayName = 'AppLayout'

  return Component
}

export default AppLayout
