import React from 'react';
import PropTypes from "prop-types";
import {Avatar, Button, Card, CardActions, CardContent, Container, TextField, Typography} from '@material-ui/core';
import withStyles from "@material-ui/core/styles/withStyles";

const styles = theme => ({
    card: {
        width: 460,
        padding: '2%',
    },
    postButton: {
        marginLeft: 'auto',
        color: '#F3FDF9',
        backgroundColor: '#4AA8E0'
    },
    paper: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        padding: 0,
    },
    avatar: {
        marginTop: '2%',
        marginRight: '5%',
        marginBottom: 'auto',
    },
    textField: {
        margin: 'auto',
    },
    form: {
        width: '100%'
    },
    header: {
        ...theme.typography.button,
        fontSize: 18,
        padding: '3px 10px',
        color: '#586269',
    },
    content: {
        padding: '10px'
    }
});

class NewPost extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            postText: '',
        }
    }

    handlePostTextChange = event => {
        event.preventDefault();
        this.setState({
            postText: event.target.value
        })
    };

    createPost = event => {
        event.preventDefault();
        if (this.state.postText.length > 0) {
            let postData = new FormData();
            postData.append('user', '6');
            postData.append('text', this.state.postText);
            this.props.addPost(postData);
            this.setState({
                postText: ''
            });
        }
    };

    render() {
        const {classes} = this.props;

        return (
            <Card className={classes.card}>
                <Typography className={classes.header}>
                    New Post
                </Typography>
                <hr/>
                <CardContent className={classes.content}>
                    <Container className={classes.paper}>
                        <Avatar className={classes.avatar}>
                            R
                        </Avatar>
                        <TextField
                            className={classes.textField}
                            variant="outlined"
                            fullWidth
                            multiline
                            rows={3}
                            onChange={this.handlePostTextChange}
                            label="Whats on your mind..."
                            name="post"
                            value={this.state.postText}
                        />
                    </Container>
                </CardContent>


                <CardActions disableSpacing>
                    <Button className={classes.postButton} onClick={this.createPost}>
                        Post
                    </Button>
                </CardActions>
            </Card>
        );
    }
}

NewPost.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(NewPost)
