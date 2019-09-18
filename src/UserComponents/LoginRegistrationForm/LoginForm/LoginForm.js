import React from 'react';
import axios from 'axios';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import PropTypes from "prop-types";
import withStyles from "@material-ui/core/styles/withStyles";

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
        marginTop: theme.spacing(4),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing(1),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
});

class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'username': '',
            'password': ''
        }
    }

    handleSubmit = event => {
        event.preventDefault();
        const body = new FormData(event.target);
        let data = {};
        body.forEach((value, name) => {
            data[name] = value;
        });
        axios.post('http://localhost:8000/api/users/rest-auth/login/', data
        ).then(response => {
            console.log(response.data);
        });
    };

    handleChange = event => {
        event.preventDefault();
        const {value, name} = event.target;
        this.setState({[name]: value});
    };

    render() {
        const {classes} = this.props;
        return (
            <Container component="main" maxWidth="xs">
                <CssBaseline/>
                <div className={classes.paper}>
                    <form className={classes.form} onSubmit={this.handleSubmit} noValidate id='loginForm'>
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Username"
                            name="username"
                            autoComplete="email"
                            autoFocus
                            value={this.state.username}
                            onChange={this.handleChange}
                        />
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            value={this.state.password}
                            onChange={this.handleChange}
                        />
                        <FormControlLabel
                            control={<Checkbox value="remember" color="primary"/>}
                            label="Remember me"
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            color="primary"
                            className={classes.submit}
                        >
                            Sign In
                        </Button>
                        <Grid container>
                            <Grid item xs>
                                <Link href="#" variant="body2">
                                    Forgot password?
                                </Link>
                            </Grid>
                        </Grid>
                    </form>
                </div>
                <Box mt={8}>
                    <Copyright/>
                </Box>
            </Container>
        );
    }
}

LoginForm.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(LoginForm);