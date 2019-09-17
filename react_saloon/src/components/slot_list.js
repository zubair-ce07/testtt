import React, { Component } from 'react'
import { connect } from 'react-redux'
import { get_time_slots_for_user } from '../actions/saloon_action'

export class SlotList extends Component {

    componentDidMount() {
        this.props.get_time_slots_for_user(this.props.match.params.shop_name);
    }

    render() {
        const { time_slots } = this.props

        const no_time_slots = ((!time_slots || time_slots.length === 0) && <div className="card" style={{ margin: '10px' }}>
            <div className="card-header">
                No Time Slots avalable
        </div>
        </div >)

        const time_slots_list = time_slots ? (
            time_slots.map((time_slot, index) => {
                const slot_date = new Date(time_slot.time)
                return (
                    <div className="card" style={{ margin: '10px', width: '100%' }} key={index}>
                        <div className="card-header">
                            {slot_date.toDateString().concat(' at ', slot_date.toLocaleTimeString())}
                        </div>
                        {time_slot.reservation === null ? (
                            <div className="card-body">
                                <button className="btn btn-primary">Reserve</button>
                            </div>
                        ) : (
                                <div className="card-body">
                                    <button className="btn btn-primary disabled">Reserved</button>
                                </div>
                            )}
                    </div>
                )
            })
        ) : (
                false
            )

        return (
            <div className='container'>
                {no_time_slots}
                {time_slots_list}
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        time_slots: state.saloon.time_slots
    }
}

const mapDispatchToProps = dispatch => {
    return {
        get_time_slots_for_user: (shop_name) => dispatch(get_time_slots_for_user(shop_name))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(SlotList)
