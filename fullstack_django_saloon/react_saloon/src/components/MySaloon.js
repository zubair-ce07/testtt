import React, { Component } from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';
import PropTypes from 'prop-types';
import { addTimeSlots, getTimeSlots } from '../actions/saloonActions';
import IsAuthenticated from '../hoc/isAuthenticated';
import $ from 'jquery';

class MySaloon extends Component {

    state = {
        start_date : '',
        end_date : ''
    }

    componentDidMount() {
        this.props.getTimeSlots();
    }

    handleSubmit = e => {
        e.preventDefault();
        this.props.addTimeSlots(this.state).then(()=>{
            if(this.props.addTimeSlotSuccessStatus){
                this.props.getTimeSlots();
                $('#modalClose').click();
            }
        });

    }

    handleChange = e => {
        let key = e.target.name;
        let val = e.target.value;
        this.setState({ [key]: val });
    }

    render() {

        const { timeSlots } = this.props;

        let date_check = this.state.start_date < this.state.end_date;
        const timeSlots_list = timeSlots.map((time_slot, index) => {
            const slot_date = new Date(time_slot.time);
            return (
                <div className="card" style={{ margin: '10px', width: '100%' }} key={index}>
                    <div className="card-header">
                        {slot_date.toDateString().concat(' at ', slot_date.toLocaleTimeString())}
                    </div>
                </div>
            );
        });


        const noTimeSlots = ((!timeSlots || timeSlots.length === 0) && <div className='container'>
            <div className="card" style={{ margin: '10px', width: '100%' }}>
                <div className="card-header">
                    No Time Slots
                </div>
                <div className="card-body">
                    <button type="button" className="btn btn-primary" data-toggle="modal" data-target="#exampleModalCenter">
                        Add Schedule
                    </button>
                </div>
            </div>
        </div >);

        const add_slots_modal = ((!timeSlots || timeSlots.length === 0) && <div className="modal fade" id="exampleModalCenter" tabIndex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle"
            aria-hidden="true">
            <div className="modal-dialog modal-dialog-centered" role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title" id="exampleModalLongTitle">Add Schedule</h5>
                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                            <span id="modalClose" aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div className="modal-body">
                        <form onSubmit={this.handleSubmit}>
                            <div className="form-group">
                                <label htmlFor="start_date">Start Date</label>
                                <input type="date" onChange={this.handleChange} className="form-control" name="start_date" id="start_date"
                                    aria-describedby="start_date_help" required />
                                <small id="Start_date_help" className="form-text text-muted">Start date for reservations.</small>
                            </div>
                            <div className="form-group">
                                <label htmlFor="end_date_help">End Date</label>
                                <input type="date" onChange={this.handleChange} className="form-control" name="end_date" id="end_date_help"
                                    aria-describedby="end_date_help_help" required />
                                <small id="end_date_help_help" className="form-text text-muted">End date for reservations.</small>
                                { !date_check && <small style={{color:'red'}}>Start date should be greater then end date.</small> }
                            </div>
                            <div className="form-group">
                                <label htmlFor="start_time">Start Time</label>
                                <div>
                                    <input type="number" onChange={this.handleChange} name="start_time" min="0" max="23" placeholder="00(hours)" required />
                                </div>
                                <small id="start_time_help" className="form-text text-muted">Shop reservations start time.</small>
                            </div>
                            <div className="form-group">
                                <label htmlFor="slot_duration">Slot duration</label>
                                <select className="form-control" onChange={this.handleChange} name="slot_duration" id="slot_duration"
                                    aria-describedby="slot_duration_help">
                                    <option value="15">15 minutes</option>
                                    <option value="30">30 minutes</option>
                                    <option value="45">45 minutes</option>
                                    <option value="60">60 minutes</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <label htmlFor="number_of_slots">Number of time slots</label>
                                <input type="number" className="form-control" min="1" max="24" name="number_of_slots"
                                    id="number_of_slots" aria-describedby="number_of_slots_help"
                                    placeholder="Enter total reservations 24 hours." onChange={this.handleChange}
                                    required />
                                { !this.props.addTimeSlotSuccessStatus && <small style={{color:'red'}}>Number of slots selected exceeds one day.</small> }
                            </div>
                            { date_check?(
                                <input type="submit" className="submit_btn btn btn-primary" value="Add"/>
                            ):(
                                <input type="submit" disabled className="submit_btn btn btn-primary" value="Add" />
                            ) }
                        </form>
                    </div>
                </div>
            </div>
        </div>);

        return (
            <React.Fragment>
                <div className='container'>
                    <h2 style={{ width: '100%', textAlign: 'center' }}>Time Slots</h2>
                    {timeSlots_list}
                </div>
                {noTimeSlots}
                {add_slots_modal}

            </React.Fragment>
        );
    }
}

MySaloon.propTypes = {
    addTimeSlots: PropTypes.func.isRequired,
    getTimeSlots: PropTypes.func.isRequired,
    timeSlots: PropTypes.array.isRequired,
    addTimeSlotSuccessStatus :PropTypes.bool.isRequired
};

const mapStateToProps = state =>
    (
        {
            timeSlots: state.saloon.timeSlots,
            addTimeSlotSuccessStatus : state.saloon.addTimeSlotSuccessStatus
        }
    );

const mapDispatchToProps = dispatch =>
    (
        {
            addTimeSlots: (data) => dispatch(addTimeSlots(data)),
            getTimeSlots: () => dispatch(getTimeSlots())
        }
    );



export default compose(
    IsAuthenticated,
    connect(mapStateToProps, mapDispatchToProps)
)(MySaloon);
