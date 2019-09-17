import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'
import ls from 'local-storage'

import { get_reservations_for_user } from '../actions/saloon_action'

export class MyReservations extends Component {

    componentDidMount() {
        const user_type = ls.get('user_type')
        if (user_type === 'customer') {
            this.props.get_reservations_for_user(this.props.match.params.shop_name)
        }
    }
    render() {
        const { reservations } = this.props
        const no_reservations = (!reservations && < div className="card" style={{ margin: '10px', width: '100%' }}>
            <div className="card-header">
                No Reservations
            </div>
            <div className="card-body">
                <Link to='/' type="button" className="btn btn-primary">
                    Reserve Now</Link>
            </div>
        </div >)

        const reservation_list = reservations ? (
            reservations.map((reservation, index) => {
                const slot_date = new Date(reservation.time_slot.time)
                return (<div className="card" style={{ margin: '10px', width: '100%' }} key={index}>
                    <div className="card-header">
                        Reservation Time : {slot_date.toDateString().concat(' at ', slot_date.toLocaleTimeString())}
                    </div>
                    <div className="card-body">
                        <h5 className="card-title">Saloon Name : {reservation.time_slot.saloon.shop_name}</h5>
                        <p className="card-text">Contact No : {reservation.time_slot.saloon.phone_no}</p>
                        <Link to='/' className="btn btn-outline-danger">Cancel reservation</Link>
                    </div>
                </div >
                )
            })
        ) : (
                false
            )

        return (
            <div className="container">
                <div className="media-body">
                    <h2 className="account-heading" style={{ textAlign: "center" }}>My Reservations</h2>
                </div>
                {no_reservations}
                {reservation_list}
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        reservations: state.saloon.reservations
    }
}

const mapDispatchToProps = dispatch => {
    return {
        get_reservations_for_user: () => dispatch(get_reservations_for_user())
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(MyReservations)
