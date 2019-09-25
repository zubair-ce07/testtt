import React, { Component } from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';
import { Link } from 'react-router-dom';
import ls from 'local-storage';
import PropTypes from 'prop-types';
import { reactAppConstants } from '../constants/constants';

import IsAuthenticated from '../hoc/isAuthenticated';
import { getReservationsForUser, cancelReservation, getSaloonReservations } from '../actions/saloonActions';

class MyReservations extends Component {

    componentDidMount() {
        const userType = ls.get(reactAppConstants.USER_TYPE);
        if (userType === reactAppConstants.CUSTOMER) {
            this.props.getReservationsForUser();
        } else if (userType === reactAppConstants.SALOON) {
            this.props.getSaloonReservations();
        }
    }

    handleCancelReservation(id) {
        this.props.cancelReservation(id);
    }

    render() {
        const { reservations } = this.props;
        const userType = ls.get(reactAppConstants.USER_TYPE);

        const reservation_list = reservations.map((reservation, index) => {
            const slot_date = new Date(reservation.time_slot.time);
            return (
                <div className="card" style={{ margin: '10px', width: '100%' }} key={index}>
                    <div className="card-header">
                        Reservation Time : {slot_date.toDateString().concat(' at ', slot_date.toLocaleTimeString())}
                    </div>
                    <div className="card-body">

                        {userType === 'customer' ? (
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
        });


        const no_reservations = ((!reservations || reservations.length === 0) && < div className="card" style={{ margin: '10px', width: '100%' }}>
            <div className="card-header">
                No Reservations
            </div>

            {userType === 'customer' && <div className="card-body">
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
    getReservationsForUser: PropTypes.func.isRequired,
    getSaloonReservations:PropTypes.func.isRequired,
    cancelReservation:PropTypes.func.isRequired

};

const mapStateToProps = (state) =>
    (
        {
            reservations: state.saloon.reservations
        }
    );

const mapDispatchToProps = dispatch =>
    (    
        {
            getReservationsForUser: () => dispatch(getReservationsForUser()),
            getSaloonReservations: () => dispatch(getSaloonReservations()),
            cancelReservation: (id) => dispatch(cancelReservation(id))
        }
    );

export default compose(
    IsAuthenticated,
    connect(mapStateToProps, mapDispatchToProps)
)(MyReservations);
