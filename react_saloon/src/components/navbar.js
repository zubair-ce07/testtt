import React from 'react'
import { Route, Switch, Link } from 'react-router-dom'
import ls from 'local-storage'

import ListSaloon from './list_saloon'
import Profile from './profile'
import my_saloon from './my_saloon'
import SlotList from './slot_list'
import MyReservations from './my_reservations'

class Navbar extends React.Component {
    nar_bar_style = {
        width: '100%'
    }

    logout = () => {
        ls.clear()
    }

    user_type = ls.get('user_type')
    token = ls.get('token')

    nav_bar_elements = this.token ? (
        <React.Fragment>
            <li className="nav-item active">
                <Link className="nav-link" to='/myreservations'> My Reservations <span className=" sr-only">(current)</span></Link>
            </li>
            {this.user_type === 'saloon' && <li className="nav-item active">
                <Link className="nav-link" to='/mysaloon'> My Saloon <span className=" sr-only">(current)</span></Link>
            </li>}
            <li className="nav-item active">
                <Link className="nav-link" to='/profile'> Profile <span className=" sr-only">(current)</span></Link>
            </li>
            <li className="nav-item active">
                <Link className="btn btn-outline-danger" onClick={this.logout} to='/login'> Logout <span className=" sr-only">(current)</span></Link>
            </li>
        </React.Fragment>
    ) : (<React.Fragment>
        <li className="nav-item active">
            <Link className="nav-link" to='/login'> Login <span className=" sr-only">(current)</span></Link>
        </li>
        <li className="nav-item active">
            <Link className="nav-link" to='/signup'>Register
    <span className=" sr-only">(current)</span></Link>
        </li>
    </React.Fragment>)

    render() {
        return (
            <div className='navbar compoent_container' >
                <nav className="navbar navbar-expand-lg navbar-primary bg-light" style={this.nar_bar_style}>
                    <Link className="navbar-brand" to="/">Saloons</Link>
                    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav mr-auto">

                        </ul>
                        <div className="form-inline my-2 my-lg-0">

                            <ul className="navbar-nav mr-auto">

                                {this.nav_bar_elements}
                            </ul>
                        </div>
                    </div>
                </nav >
                <Switch>
                    <Route exact path='/' component={ListSaloon} />
                    <Route exact path='/profile/' component={Profile} />
                    <Route exact path='/mysaloon/' component={my_saloon} />
                    <Route exact path='/myreservations/' component={MyReservations} />
                    <Route path="/:shop_name/" component={SlotList} />
                </Switch>
            </div >

        )
    }


}

export default Navbar