import React, { Component } from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Container from '@material-ui/core/Container';
import IsAuthenticated from '../hoc/isAuthenticated';
import { getTimeSlotsForUser, reserveSlotForUser } from '../actions/saloonActions';

export class SlotList extends Component {

    componentDidMount() {
        this.props.getTimeSlotsForUser(this.props.match.params.shop_name);
    }

    handleReserveClick = id => {
        this.props.reserveSlotForUser(id);
    }

    render() {
        const { timeSlots } = this.props;

        const noTimeSlots = ((!timeSlots || timeSlots.length === 0) && <Card style={{ margin: '10px' }}>
            <CardContent className="card-header">
                <Typography gutterBottom variant="h5" component="h2">
                    No Time Slots Available
                </Typography>
            </CardContent>
        </Card >);

        const timeSlotsList = timeSlots.map((time_slot, index) => {
            const slot_date = new Date(time_slot.time);
            return (
                <Card style={{ margin: '10px', width: '100%' }} key={index}>
                    <CardContent className="card-header">
                        <Typography gutterBottom variant="h5" component="h2">
                            {slot_date.toDateString().concat(' at ', slot_date.getUTCHours(),':',slot_date.getUTCMinutes())}
                        </Typography>
                        {time_slot.reservation === null ? (
                            <Button onClick={() => this.handleReserveClick(time_slot.id)} variant="contained" size="small" color="primary" >Reserve</Button>
                        ) : (
                            <Button size="small" variant="contained" disabled color="primary" >Reserved</Button>
                        )}
                    </CardContent>
                </Card>
            );
        });

        return (
            <Container>
                {noTimeSlots}
                {timeSlotsList}
            </Container>
        );
    }
}

SlotList.propTypes = {
    timeSlots: PropTypes.array.isRequired,
    getTimeSlotsForUser:PropTypes.func.isRequired,
    reserveSlotForUser:PropTypes.func.isRequired,
    match:PropTypes.object.isRequired
};

const mapStateToProps = state => ({
    timeSlots: state.saloon.timeSlots
});

const mapDispatchToProps = dispatch => ({
    getTimeSlotsForUser: (shop_name) => dispatch(getTimeSlotsForUser(shop_name)),
    reserveSlotForUser: (id) => dispatch(reserveSlotForUser(id))
});

export default compose(
    IsAuthenticated,
    connect(mapStateToProps, mapDispatchToProps)
)(SlotList);
