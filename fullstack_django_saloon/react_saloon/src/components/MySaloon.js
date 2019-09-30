import React, { Component } from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';
import PropTypes from 'prop-types';
import { addTimeSlots, getTimeSlots } from '../actions/saloonActions';
import IsAuthenticated from '../hoc/isAuthenticated';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import withStyles from '@material-ui/styles/withStyles';
import { appStyles } from '../styles/appStyles';
import { Field, reduxForm } from 'redux-form';
import {renderField,renderSelectField,validate} from './RenderField';

class MySaloon extends Component {

    constructor(props) {
        super(props);
        this.state = {
            open:false
        };
    }

    componentDidMount() {
        this.props.getTimeSlots();
    }

    formSubmit = values => {
        this.props.addTimeSlots(values).then(() => {
            if(this.props.addTimeSlotSuccessStatus){
                this.props.getTimeSlots();
                this.setState({open:false});
            }
        });

    }

    handleToggle = () => {
        this.setState({
            open: !this.state.open
        });
    };

    render() {
        const { classes } = this.props;
        const { timeSlots } = this.props;
        const { handleSubmit} = this.props;
        const { invalid } = this.props;
        const timeSlots_list = timeSlots.map((time_slot, index) => {
            const slot_date = new Date(time_slot.time);
            return (
                <Card className={classes.cardStyle} key={index}>
                    <CardContent className="card-header">
                        <Typography gutterBottom variant="h5" component="h2">
                            {slot_date.toDateString().concat(' at ', slot_date.getUTCHours(),':',slot_date.getUTCMinutes())}
                        </Typography>
                    </CardContent>
                </Card>
            );
        });

        const noTimeSlots = ((!timeSlots || timeSlots.length === 0) && <React.Fragment>
            <Card className={classes.cardStyle}>
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
                    <form onSubmit={handleSubmit(this.formSubmit)}>
                        <Field
                            id="start_date"
                            label="Start Date"
                            name="start_date"
                            className={classes.textFieldStyle}
                            required
                            component={renderField}
                            value={this.state.start_date}
                            type='date'
                        />
                        <Field
                            id="end_date"
                            label="End Date"
                            name="end_date"
                            className={classes.textFieldStyle}
                            required
                            component={renderField}
                            type='date'
                        />
                        <Field
                            id="start_time"
                            label="Start Time"
                            name="start_time"
                            className={classes.textFieldStyle}
                            required
                            component={renderField}
                            min='0'
                            max = '23'
                            type='number'
                        />
                        <FormControl className={classes.textFieldStyle}>
                            <InputLabel htmlFor="slot_duration">Slot Duration</InputLabel>
                            <Field
                                id="slot_duration"
                                name="slot_duration"
                                required
                                component={renderSelectField}
                            />
                        </FormControl>

                        <Field
                            id="number_of_slots"
                            label="Number of slots in a day"
                            name="number_of_slots"
                            required
                            component={renderField}
                            className={classes.textFieldStyle}
                            type='number'
                        />
                        { !this.props.addTimeSlotSuccessStatus && <Typography variant="h6" style={{color:'red'}}>
                            Number of slots selected exceeds one day.
                        </Typography>}
                        
                        <Button type="submit" disabled={invalid} variant="contained" color="primary">
                        Add
                        </Button>
                    </form>
                </DialogContent>
            </Dialog>);

        return (
            <React.Fragment>
                <Container>
                    <h2 className={classes.timeSlotHeading}>Time Slots</h2>
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
    addTimeSlotSuccessStatus :PropTypes.bool.isRequired,
    handleSubmit:PropTypes.func.isRequired,
    invalid:PropTypes.bool.isRequired,
    classes:PropTypes.object.isRequired
};

const mapStateToProps = state => ({
    timeSlots: state.saloon.timeSlots,
    addTimeSlotSuccessStatus : state.saloon.addTimeSlotSuccessStatus
});

const mapDispatchToProps = dispatch => ({
    addTimeSlots: (data) => dispatch(addTimeSlots(data)),
    getTimeSlots: () => dispatch(getTimeSlots())
});

export default compose(
    connect(mapStateToProps, mapDispatchToProps),
    IsAuthenticated,
    reduxForm({
        form: 'signupForm',
        validate:validate,
    }),
    withStyles(appStyles)
)(MySaloon);