import React, { Component } from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';
import { Link } from 'react-router-dom';
import localStorage from 'local-storage';
import PropTypes from 'prop-types';
import { reactAppConstants } from '../constants/constants';
import { routeConstants } from '../constants/routeConstants';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Container from '@material-ui/core/Container';

import IsAuthenticated from '../hoc/isAuthenticated';
import { getReservationsForUser, cancelReservation, getSaloonReservations } from '../actions/saloonActions';

class MyReservations extends Component {

    componentDidMount() {
        const userType = localStorage.get(reactAppConstants.USER_TYPE);
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
        const userType = localStorage.get(reactAppConstants.USER_TYPE);

        const reservation_list = reservations.map((reservation, index) => {
            const slot_date = new Date(reservation.time_slot.time);
            return (
                <Card style={{ margin: '10px', width: '100%' }} key={index}>
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                        Reservation Time : {slot_date.toDateString().concat(' at ', slot_date.getUTCHours(),':',slot_date.getUTCMinutes())}
                        </Typography>
                        {userType === reactAppConstants.CUSTOMER ? (
                            <React.Fragment>
                                <Typography variant="h6" component="h2">
                                    Saloon Name : {reservation.time_slot.saloon.shop_name}
                                </Typography>
                                <Typography variant="h6" component="h2">
                                    Contact No : {reservation.time_slot.saloon.phone_no}
                                </Typography>
                            </React.Fragment>
                        ) : (
                            <React.Fragment>
                                <Typography variant="h6" component="h2">
                                    Customer Name : {reservation.customer.user.first_name}
                                </Typography>
                                <Typography variant="h6" component="h2">
                                    Contact No : {reservation.customer.phone_no}
                                </Typography>
                            </React.Fragment>
                        )}

                        <Button size="small" variant="contained" color="secondary" onClick={() => this.handleCancelReservation(reservation.id)}>Cancel reservation</Button>
                    </CardContent>
                </Card >
            );
        });


        const no_reservations = ((!reservations || reservations.length === 0) && <Card style={{ margin: '10px', width: '100%' }}>
            <Typography variant="h6" component="h2">
                No Reservations
            </Typography>

            {userType === 'customer' &&<CardContent>
                <Button to={routeConstants.LIST_SALOONS_ROUTE} variant='contained' color='primary'>
                    <Link to={routeConstants.LIST_SALOONS_ROUTE}
                        style={{ textDecoration: 'none',color:'white' }}>
                        Reserve Now
                    </Link>
                </Button>
            </CardContent>}
        </Card >);


        return (
            <Container>
                <Typography variant="h4" style={{textAlign:'center'}} component="h2">
                    My Reservations
                </Typography>
                {no_reservations}
                {reservation_list}
            </Container>
        );
    }
}

MyReservations.propTypes = {
    reservations: PropTypes.array.isRequired,
    getReservationsForUser: PropTypes.func.isRequired,
    getSaloonReservations:PropTypes.func.isRequired,
    cancelReservation:PropTypes.func.isRequired

};

const mapStateToProps = (state) => ({
    reservations: state.saloon.reservations
});

const mapDispatchToProps = dispatch => ({
    getReservationsForUser: () => dispatch(getReservationsForUser()),
    getSaloonReservations: () => dispatch(getSaloonReservations()),
    cancelReservation: (id) => dispatch(cancelReservation(id))
});

export default compose(
    IsAuthenticated,
    connect(mapStateToProps, mapDispatchToProps)
)(MyReservations);
