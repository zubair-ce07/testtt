import React from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import PropTypes from "prop-types";
import withStyles from "@material-ui/core/styles/withStyles";
import 'date-fns';
import DateFnsUtils from '@date-io/date-fns';
import {
    MuiPickersUtilsProvider,
    KeyboardDatePicker,
} from '@material-ui/pickers';
import axios from "axios";

function Copyright() {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {'Copyright © '}
            Social App
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

const styles = theme => ({
    '@global': {
        body: {
            backgroundColor: theme.palette.common.white,
        },
    },
    paper: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing(3),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
});

class SignUpForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        }
    }

    handleSubmit = event => {
        event.preventDefault();
        const body = new FormData(event.target);
        let data = {};
        body.forEach((value, name) => {
            data[name] = value;
        });
        axios.post('http://localhost:8000/api/users/', data
        ).then(response => {
            alert(response);
        });
    };

    handleChange = event => {
        event.preventDefault();
        const {value, name} = event.target;
        this.setState({ [name]: value});
    };

    render() {
        const {classes} = this.props;

        return (
            <Container component="main" maxWidth="xs">
                <CssBaseline/>
                <div className={classes.paper}>
                    <form className={classes.form} onSubmit={this.handleSubmit} noValidate>
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    label="First Name"
                                    name='first_name'
                                    autoFocus
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    label="Last Name"
                                    name="last_name"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    label="Username"
                                    name="username"
                                    autoComplete="username"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    label="Email Address"
                                    name="email"
                                    autoComplete="email"
                                />
                            </Grid>

                            <MuiPickersUtilsProvider utils={DateFnsUtils}>
                                <Grid item xs={12}>
                                    <KeyboardDatePicker
                                        disableToolbar
                                        variant="inline"
                                        format="yyyy-MM-dd"
                                        margin="normal"
                                        fullWidth
                                        name='date_of_birth'
                                        label="Date of Birth"
                                        KeyboardButtonProps={{
                                            'aria-label': 'change date',
                                        }}
                                    />
                                </Grid>
                            </MuiPickersUtilsProvider>
                            <Grid item xs={12}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    name="phone"
                                    label="Phone"
                                    type="phone"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    variant="outlined"
                                    required
                                    multiline
                                    rows={2}
                                    fullWidth
                                    name="address"
                                    label="Address"
                                    type="address"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    name="password"
                                    label="Password"
                                    type="password"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    variant="outlined"
                                    required
                                    fullWidth
                                    name="password2"
                                    label="Confirm Password"
                                    type="password"
                                />
                            </Grid>
                        </Grid>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            color="primary"
                            className={classes.submit}
                        >
                            Sign Up
                        </Button>
                    </form>
                </div>
                <Box mt={1}>
                    <Copyright/>
                </Box>
            </Container>
        );
    }
}

SignUpForm.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SignUpForm)