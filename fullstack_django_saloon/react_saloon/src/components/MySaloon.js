import React, { Component } from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';
import PropTypes from 'prop-types';
import { addTimeSlots, getTimeSlots } from '../actions/saloonActions';
import IsAuthenticated from '../hoc/isAuthenticated';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import { Container } from '@material-ui/core';
import {
    Button,
    Dialog,
    DialogContent,
    DialogContentText,
    DialogTitle
} from '@material-ui/core';
import TextField from '@material-ui/core/TextField';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

class MySaloon extends Component {
    state = {
        start_date :'',
        end_date : '',
        slot_duration: '60',
        open:false
    }
    textFiledStyle = {
        width: '100%'
    }

    componentDidMount() {
        this.props.getTimeSlots();
    }

    handleSubmit = e => {
        e.preventDefault();
        this.props.addTimeSlots(this.state).then(()=>{
            console.log(this.props.addTimeSlotSuccessStatus);
            if(this.props.addTimeSlotSuccessStatus){
                this.props.getTimeSlots();
                this.setState({open:false});
            }
        });

    }

    handleChange = e => {
        let key = e.target.name;
        let val = e.target.value;
        this.setState({ [key]: val });
    }

    handleToggle = () => {
        this.setState({
            open: !this.state.open
        });
    };

    render() {

        const { timeSlots } = this.props;

        let date_check = this.state.start_date <= this.state.end_date;
        const timeSlots_list = timeSlots.map((time_slot, index) => {
            const slot_date = new Date(time_slot.time);
            return (
                <Card style={{ margin: '10px', width: '100%' }} key={index}>
                    <CardContent className="card-header">
                        <Typography gutterBottom variant="h5" component="h2">
                            {slot_date.toDateString().concat(' at ', slot_date.getUTCHours(),':',slot_date.getUTCMinutes())}
                        </Typography>
                    </CardContent>
                </Card>
            );
        });


        const noTimeSlots = ((!timeSlots || timeSlots.length === 0) && <React.Fragment>
            <Card style={{ margin: '10px', width: '100%' }}>
                <CardContent className="card-header">
                    <Typography gutterBottom variant="h5" component="h2">
                        Time Slots Not Available
                    </Typography>
                    <Button onClick={this.handleToggle} variant="contained" color="primary">
                        Add Schedule
                    </Button>
                </CardContent>
            </Card>
        </React.Fragment >);

        const add_slots_modal = ((!timeSlots || timeSlots.length === 0) &&
            <Dialog
                open={this.state.open}
                onClose={this.handleToggle}
            >
                <DialogTitle>
                    Add Schedule for Time Slots
                </DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Please fill out the form below.
                    </DialogContentText>
                    <form onSubmit={this.handleSubmit}>
                        <TextField
                            id="start_date"
                            label="Start Date"
                            name="start_date"
                            style={this.textFiledStyle}
                            required
                            value={this.state.start_date}
                            onChange={this.handleChange}
                            margin="normal"
                            variant="outlined"
                            type='date'
                        />
                        <TextField
                            id="end_date"
                            label="End Date"
                            name="end_date"
                            style={this.textFiledStyle}
                            required
                            onChange={this.handleChange}
                            margin="normal"
                            variant="outlined"
                            type='date'
                        />
                        { !date_check && <Typography variant="h6" style={{color:'red'}}>
                            Start date should be greater then end date.
                        </Typography>}
                        <TextField
                            id="start_time"
                            label="Start Time"
                            name="start_time"
                            required
                            style={this.textFiledStyle}
                            onChange={this.handleChange}
                            margin="normal"
                            variant="outlined"
                            min='0'
                            max = '23'
                            type='number'
                        />
                        <FormControl style={this.textFiledStyle}>
                            <InputLabel htmlFor="slot_duration">Slot Duration</InputLabel>
                            <Select
                                required
                                value={this.state.slot_duration}
                                name="slot_duration"
                                id="slot_duration"
                                onChange={this.handleChange}
                            >
                                <MenuItem value={'15'}>15 minutes</MenuItem>
                                <MenuItem value={'30'}>30 minutes</MenuItem>
                                <MenuItem value={'45'}>45 minutes</MenuItem>
                                <MenuItem value={'60'}>60 minutes</MenuItem>
                            </Select>
                        </FormControl>

                        <TextField
                            id="number_of_slots"
                            label="Number of slots in a day"
                            name="number_of_slots"
                            style={this.textFiledStyle}
                            required
                            onChange={this.handleChange}
                            margin="normal"
                            variant="outlined"
                            type='number'
                        />
                        { !this.props.addTimeSlotSuccessStatus && <Typography variant="h6" style={{color:'red'}}>
                            Number of slots selected exceeds one day.
                        </Typography>}
                        
                        { date_check?(
                            <Button type="submit" variant="contained" color="primary">
                            Add
                            </Button>
                        ):(
                            <Button type="submit" variant="contained" disabled color="primary">
                            Add
                            </Button>
                        ) }
                    </form>
                </DialogContent>
            </Dialog>);

        return (
            <React.Fragment>
                <Container>
                    <h2 style={{ width: '100%', textAlign: 'center' }}>Time Slots</h2>
                    {timeSlots_list}
                    {noTimeSlots}
                    {add_slots_modal}
                </Container>
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
