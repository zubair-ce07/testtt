import React, { Component } from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';
import { Link } from 'react-router-dom';
import ls from 'local-storage';
import PropTypes from 'prop-types';

import IsAuthenticated from '../hoc/isAuthenticated';
import { get_reservations_for_user, cancel_reservation, get_saloon_reservations } from '../actions/saloonActions';

class MyReservations extends Component {

    componentDidMount() {
        const user_type = ls.get('user_type');
        if (user_type === 'customer') {
            this.props.get_reservations_for_user();
        } else if (user_type === 'saloon') {
            this.props.get_saloon_reservations();
        }
    }

    handleCancelReservation(id) {
        this.props.cancel_reservation(id);
    }

    render() {
        const { reservations } = this.props;
        const user_type = ls.get('user_type');

        const reservation_list = reservations ? (
            reservations.map((reservation, index) => {
                const slot_date = new Date(reservation.time_slot.time);
                return (<div className="card" style={{ margin: '10px', width: '100%' }} key={index}>
                    <div className="card-header">
                        Reservation Time : {slot_date.toDateString().concat(' at ', slot_date.toLocaleTimeString())}
                    </div>
                    <div className="card-body">

                        {user_type === 'customer' ? (
                            <React.Fragment>
                                <h5 className="card-title">Saloon Name : {reservation.time_slot.saloon.shop_name}</h5>
                                <p className="card-text">Contact No : {reservation.time_slot.saloon.phone_no}</p>
                            </React.Fragment>
                        ) : (
                            <React.Fragment>
                                <h5 className="card-title">Customer Name : {reservation.customer.user.first_name}</h5>
                                <p className="card-text">Contact No : {reservation.customer.phone_no}</p>
                            </React.Fragment>
                        )}

                        <button className="btn btn-outline-danger" onClick={() => this.handleCancelReservation(reservation.id)}>Cancel reservation</button>
                    </div>
                </div >
                );
            })
        ) : (
            false
        );



        const no_reservations = ((!reservations || reservations.length === 0) && < div className="card" style={{ margin: '10px', width: '100%' }}>
            <div className="card-header">
                No Reservations
            </div>

            {user_type === 'customer' && <div className="card-body">
                <Link to='/' className="btn btn-primary">
                    Reserve Now</Link>
            </div>}
        </div >);


        return (
            <div className="container">
                <div className="media-body">
                    <h2 className="account-heading" style={{ textAlign: 'center' }}>My Reservations</h2>
                </div>
                {no_reservations}
                {reservation_list}
            </div>
        );
    }
}

MyReservations.propTypes = {
    reservations: PropTypes.array.isRequired,
    get_reservations_for_user: PropTypes.func.isRequired,
    get_saloon_reservations:PropTypes.func.isRequired,
    cancel_reservation:PropTypes.func.isRequired

};

const mapStateToProps = (state) => {
    return {
        reservations: state.saloon.reservations
    };
};

const mapDispatchToProps = dispatch => {
    return {
        get_reservations_for_user: () => dispatch(get_reservations_for_user()),
        get_saloon_reservations: () => dispatch(get_saloon_reservations()),
        cancel_reservation: (id) => dispatch(cancel_reservation(id))
    };
};

export default compose(
    IsAuthenticated,
    connect(mapStateToProps, mapDispatchToProps)
)(MyReservations);
