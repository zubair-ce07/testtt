import React, { Component } from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';
import PropTypes from 'prop-types';

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

        const noTimeSlots = ((!timeSlots || timeSlots.length === 0) && <div className="card" style={{ margin: '10px' }}>
            <div className="card-header">
                No Time Slots avalable
            </div>
        </div >);

        const timeSlotsList = timeSlots.map((time_slot, index) => {
            const slot_date = new Date(time_slot.time);
            return (
                <div className="card" style={{ margin: '10px', width: '100%' }} key={index}>
                    <div className="card-header">
                        {slot_date.toDateString().concat(' at ', slot_date.toLocaleTimeString())}
                    </div>
                    {time_slot.reservation === null ? (
                        <div className="card-body">
                            <button onClick={() => this.handleReserveClick(time_slot.id)} className="btn btn-primary">Reserve</button>
                        </div>
                    ) : (
                        <div className="card-body">
                            <button className="btn btn-primary disabled">Reserved</button>
                        </div>
                    )}
                </div>
            );
        });

        return (
            <div className='container'>
                {noTimeSlots}
                {timeSlotsList}
            </div>
        );
    }
}

SlotList.propTypes = {
    timeSlots: PropTypes.array.isRequired,
    getTimeSlotsForUser:PropTypes.func.isRequired,
    reserveSlotForUser:PropTypes.func.isRequired,
    match:PropTypes.object.isRequired
};

const mapStateToProps = state =>
    (
        {
            timeSlots: state.saloon.timeSlots
        }
    );

const mapDispatchToProps = dispatch => 
    (
        {
            getTimeSlotsForUser: (shop_name) => dispatch(getTimeSlotsForUser(shop_name)),
            reserveSlotForUser: (id) => dispatch(reserveSlotForUser(id))
        }
    );

export default compose(
    IsAuthenticated,
    connect(mapStateToProps, mapDispatchToProps)
)(SlotList);
