import React from 'react';
import PropTypes from "prop-types";
import {Box, Button, Container, CssBaseline, Grid, Link, TextField} from '@material-ui/core';
import withStyles from "@material-ui/core/styles/withStyles";
import {Copyright} from "../../Utils/Utils";
import {loginAPI, logoutAPI} from "../../APIClient/APIClient";

const styles = theme => ({
    container: {
        marginLeft: 0,
        marginRight: 0,
        marginTop: theme.spacing(4),
    },
    paper: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    form: {
        width: '100%',
        marginTop: theme.spacing(1),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },

});

class LoginForm extends React.Component {
    handleSubmit = event => {
        event.preventDefault();
        const body = new FormData(event.target);
        let data = {};
        body.forEach((value, name) => {
            data[name] = value;
        });
        loginAPI(data).then(response => {
            this.props.handleUser(response.data.user, response.data.token)
        });
    };

    render() {
        const {classes} = this.props;
        return (
            <Container>
                <CssBaseline />
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
                                <Link href="#" variant="body2" >
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
