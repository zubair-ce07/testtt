import React from 'react'
import { Route, Switch, Link } from 'react-router-dom'

import ListSaloon from './list_saloon'

const Navbar = () => {
    let nar_bar_style = {
        width: '100%'
    }
    return (
        <div className='navbar compoent_container'>
            <nav className="navbar navbar-expand-lg navbar-primary bg-light" style={nar_bar_style}>
                <a className="navbar-brand" href="{% url 'shop_list' %}">Saloons</a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">

                    </ul>
                    <div className="form-inline my-2 my-lg-0">

                        <ul className="navbar-nav mr-auto">
                            {/* <li className="nav-item active">
                                <a className="nav-link" href="{% url 'my_shop' %}">My Saloon<span
                                    className="sr-only">(current)</span></a>
                            </li>
                            <li className="nav-item active">
                                <a className="nav-link" href="{% url 'shop_reservations' %}">Reservations<span
                                    className="sr-only">(current)</span></a>
                            </li>
                            <li className="nav-item active">
                                <a className="nav-link" href="{% url 'shop_profile' %}">Profile<span
                                    className="sr-only">(current)</span></a>
                            </li>
                            <li className="nav-item active">
                                <a className="nav-link" href="{% url 'customer_profile' %}">Profile<span
                                    className="sr-only">(current)</span></a>
                            </li>
                            <li className="nav-item active">
                                <a className="nav-link" href="{% url 'customer_reservations' %}">My Reservations<span
                                    className="sr-only">(current)</span></a>
                            </li>
                            <li className="nav-item active">
                                <a className="btn btn-outline-danger" href="{% url 'logout' %}">logout<span
                                    className="sr-only">(current)</span></a>
                            </li> */}
                            <li className="nav-item active">
                                <Link className="nav-link" to='/login'> Login <span className=" sr-only">(current)</span></Link>
                            </li>
                            <li className="nav-item active">
                                <Link className="nav-link" to='/signup'>Register
                                <span className=" sr-only">(current)</span></Link>
                            </li>

                        </ul>
                    </div>
                </div>
            </nav >
            <Switch>
                <Route path='/' component={ListSaloon} />
            </Switch>
        </div >

    )
}

export default Navbar