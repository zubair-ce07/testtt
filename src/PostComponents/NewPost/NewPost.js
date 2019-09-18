import React from 'react';
import {
    Card,
    CardActions,
    CardContent,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    IconButton,
    TextField,
    Typography
} from '@material-ui/core';
import {AddPhotoAlternate,} from '@material-ui/icons';
import PropTypes from "prop-types";
import withStyles from "@material-ui/core/styles/withStyles";
import Button from "@material-ui/core/Button";
import Avatar from "@material-ui/core/Avatar";
import Container from "@material-ui/core/Container";

import Image from 'material-ui-image'
import ImageUploader from 'react-images-upload';

const styles = theme => ({
    card: {
        width: 460,
        padding: '2%',
    },
    post_button: {
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
    text_field: {
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
            'dialog': false,
            'image': null,
        }
    }


    handleImageUploadDialogOpen = () => {
        this.setState({'dialog': true});
    };

    handleImageUploadDialogClose = () => {
        this.setState({
            'dialog': false,
            'image': null
        });
    };

    handleImageAdd = event => {
        this.setState({
            'image': URL.createObjectURL(event.target.files[0])
        })
    };


    handleAttachPicture = () => {

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

                        </Avatar>
                        <form className={classes.form}>
                            <TextField
                                className={classes.text_field}
                                variant="outlined"
                                fullWidth
                                multiline
                                rows={3}
                                label="Whats on your mind..."
                                name="post"
                            />
                        </form>
                    </Container>

                </CardContent>

                <CardActions disableSpacing>
                    <IconButton aria-label="upload" title='Upload' onClick={this.handleImageUploadDialogOpen}>
                        <AddPhotoAlternate/>
                    </IconButton>
                    <Dialog open={this.state.dialog} onClose={this.handleImageUploadDialogClose}
                            aria-labelledby="form-dialog-title"
                            maxWidth='sm' fullWidth={true}>
                        <DialogTitle id="form-dialog-title">Upload a Picture</DialogTitle>
                        <DialogContent>

                            {this.state.image != null ?
                                <div>
                                    <Image src={this.state.image} aspectRatio={4/3} />
                                    <br/>
                                </div>
                                  : null}

                            <input type='file' onChange={this.handleImageAdd} />

                        </DialogContent>
                        <DialogActions>
                            <Button onClick={this.handleImageUploadDialogClose} color="primary">
                                Cancel
                            </Button>
                            <Button onClick={this.handleImageUploadDialogClose} color="primary">
                                Upload
                            </Button>
                        </DialogActions>
                    </Dialog>

                    <Button className={classes.post_button}>
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