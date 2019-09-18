import React, { Component } from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';
import PropTypes from 'prop-types';

import isAuthneticated from '../hoc/isAuthenticated';
import { get_time_slots_for_user, reserve_slot_for_user } from '../actions/saloon_action';

export class SlotList extends Component {

    componentDidMount() {
        this.props.get_time_slots_for_user(this.props.match.params.shop_name);
    }

    handleReserveClick = (id) => {
        this.props.reserve_slot_for_user(id);
    }

    render() {
        const { time_slots } = this.props;

        const no_time_slots = ((!time_slots || time_slots.length === 0) && <div className="card" style={{ margin: '10px' }}>
            <div className="card-header">
                No Time Slots avalable
            </div>
        </div >);

        const time_slots_list = time_slots ? (
            time_slots.map((time_slot, index) => {
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
            })
        ) : (
            false
        );

        return (
            <div className='container'>
                {no_time_slots}
                {time_slots_list}
            </div>
        );
    }
}

SlotList.propTypes = {
    time_slots: PropTypes.array.isRequired,
    successStatus: PropTypes.bool.isRequired,
    get_time_slots_for_user:PropTypes.func.isRequired,
    reserve_slot_for_user:PropTypes.func.isRequired,
    match:PropTypes.object.isRequired,
    'match.params':PropTypes.object.isRequired,
    'match.params.shop_name':PropTypes.isRequired
};

const mapStateToProps = (state) => {
    return {
        time_slots: state.saloon.time_slots,
        successStatus: state.successStatus
    };
};

const mapDispatchToProps = dispatch => {
    return {
        get_time_slots_for_user: (shop_name) => dispatch(get_time_slots_for_user(shop_name)),
        reserve_slot_for_user: (id) => dispatch(reserve_slot_for_user(id))
    };
};

export default compose(
    isAuthneticated,
    connect(mapStateToProps, mapDispatchToProps)
)(SlotList);
