import React from "react";
import {
    Avatar,
    Button,
    Typography,
    Grid,
    ListItem,
    Dialog,
    DialogTitle,
    DialogActions
} from "@material-ui/core";

class CommentListItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            openConfirmation: false
        }
    }

    handleDeleteConfirmationDialogOpen = () => {
        this.setState({
            openConfirmation: true
        })
    };

    handleDeleteConfirmationDialogClose = () => {
        this.setState({
            openConfirmation: false
        })
    };

    deleteComment = () => {
        this.props.removeComment(this.props.comment);
        this.handleDeleteConfirmationDialogClose();
    };

    render() {
        return (
            <ListItem>
                <Grid
                    container
                    direction="row"
                    justify="flex-start"
                    alignItems="center"
                >
                    <Grid
                        item
                        xs={2}
                    >
                        <Avatar>
                            {
                                this.props.comment ?
                                this.props.comment.user.first_name[0] :
                                null
                            }
                        </Avatar>
                    </Grid>
                    <Grid
                        item
                        xs
                        container
                        direction="column"
                    >
                        <Typography variant="subtitle2">
                            {this.props.comment.user.first_name + ' ' + this.props.comment.user.last_name}
                        </Typography>
                        <Typography variant="caption">
                            {this.props.comment.text}
                        </Typography>
                    </Grid>
                    {
                        this.props.comment.user.id === 2 ?
                            <Button onClick={this.handleDeleteConfirmationDialogOpen}>
                                Delete
                            </Button> :
                            null
                    }
                    <Dialog
                        open={this.state.openConfirmation}
                        onClose={this.handleDeleteConfirmationDialogClose}
                        fullWidth
                        maxWidth='xs'
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"
                    >
                        <DialogTitle id="alert-dialog-title">{"Delete Comment?"}</DialogTitle>
                        <DialogActions>
                            <Button onClick={this.handleDeleteConfirmationDialogClose} color="primary" autoFocus>
                                Cancel
                            </Button>
                            <Button onClick={this.deleteComment} color="secondary">
                                Delete
                            </Button>
                        </DialogActions>
                    </Dialog>
                </Grid>
            </ListItem>
        );
    }
}

export default CommentListItem;
