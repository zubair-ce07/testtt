import React from 'react';
import PropTypes from "prop-types";
import {
    Avatar,
    Button,
    Card,
    CardActions,
    CardContent,
    CardHeader,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Divider,
    Grid,
    IconButton,
    Link,
    List,
    ListItem,
    Popover,
    TextField,
    Typography
} from '@material-ui/core';
import {Comment, MoreVert,} from '@material-ui/icons';
import withStyles from "@material-ui/core/styles/withStyles";
import CommentListItem from './CommentListItem'
import {createCommentDB, deleteCommentDB, fetchCommentsDB} from '../../APIClient/APIClient'
import Vote from "./Vote";
import {formatDate} from "../../Utils/Utils";

//TODO
//fetch user with comments in some way while creating comments

const styles = theme => ({
    card: {
        width: 460,
    },
    commentDelete: {
        float: 'right'
    },
});

class Post extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            profile: 'https://avatoon.net/wp-content/uploads/2019/05/Szilagyi-Zoltan-Avatar-Small-300x300.jpg',
            dialog: false,
            openOptions: false,
            anchorEl: null,
            showCommentsDialog: false,
            openConfirmation: false,
            comments: [],
            commentText: ''
        }

    }

    handleStateChange = (newValue) => {
        this.setState({
            ...newValue
        })
    };

    deletePost = () => {
        this.props.removePost(this.props.data);
        this.handleStateChange({openConfirmation: false});
        this.handleStateChange({
            openOptions: false,
            anchorEl: null
        })
    };

    deleteComment = comment => {
        deleteCommentDB(comment).then(response => {
            this.setState(state => {
                const comments = state.comments.filter(existingComment => {
                    return comment.id !== existingComment.id
                });
                return {
                    comments: comments
                }
            });
        })
    };

    createComment = () => {
        let data = {
            user: 6,
            post: this.props.data.id,
            text: this.state.commentText
        };
        createCommentDB(this.props.data, data).then(response => {
            this.setState(state => {
                const comments = state.comments.concat(response.data);
                return {
                    comments,
                    commentText: ''
                }
            });
            this.handleStateChange({dialog: false});
        })
    };

    fetchComments = () => {
        fetchCommentsDB(this.props.data).then(response => {
            this.setState({
                comments: response.data
            });
        })
    };

    componentDidMount() {
        this.fetchComments(this.props.data);
        setInterval(() => {
            this.fetchComments(this.props.data);
        }, 5000);
    }

    componentWillUnmount() {
        clearInterval();
    }

    render() {
        const {classes} = this.props;

        return (
            <Card className={classes.card}>
                <CardHeader
                    avatar={
                        <Avatar className={classes.avatar} src={this.state.profile}/>
                    }
                    action={
                        <div>
                            <IconButton aria-label="settings" onClick={event => {
                                event.preventDefault();
                                this.handleStateChange({
                                    openOptions: true,
                                    anchorEl: event.currentTarget
                                })
                            }}>
                                <MoreVert/>
                            </IconButton>
                            <Popover
                                open={this.state.openOptions}
                                onClose={() => {
                                    this.handleStateChange({
                                        openOptions: false,
                                        anchorEl: null
                                    })
                                }}
                                anchorEl={this.state.anchorEl}
                                anchorOrigin={{
                                    vertical: 'bottom',
                                    horizontal: 'center',
                                }}
                                transformOrigin={{
                                    vertical: 'top',
                                    horizontal: 'center',
                                }}>
                                <List>
                                    <ListItem>
                                        <Button onClick={() => {
                                            this.handleStateChange({openConfirmation: true})
                                        }}>
                                            Delete
                                        </Button>
                                    </ListItem>
                                </List>
                            </Popover>

                            <Dialog
                                open={this.state.openConfirmation}
                                onClose={() => {
                                    this.handleStateChange({openConfirmation: false})
                                }}
                                fullWidth
                                maxWidth='xs'
                                aria-labelledby="alert-dialog-title"
                                aria-describedby="alert-dialog-description"
                            >
                                <DialogTitle id="alert-dialog-title">{"Delete Post?"}</DialogTitle>
                                <DialogActions>
                                    <Button onClick={() => {
                                        this.handleStateChange({openConfirmation: false})
                                    }} color="primary"
                                            autoFocus>
                                        Cancel
                                    </Button>
                                    <Button onClick={this.deletePost} color="secondary">
                                        Delete
                                    </Button>
                                </DialogActions>
                            </Dialog>
                        </div>
                    }
                    title={this.props.data.user.first_name + ' ' + this.props.data.user.last_name}
                    subheader={formatDate(new Date(this.props.data.created_at))}
                />

                <CardContent>
                    <Typography variant="body2" color="textPrimary" component="p">
                        {this.props.data.text}
                    </Typography>
                    <br/>
                    <Typography variant="overline" color="textSecondary" display="block" gutterBottom>
                        <Link color='inherit' component="button" variant="overline"
                              onClick={() => {
                                  this.handleStateChange({showCommentsDialog: true})
                              }}>
                            {this.state.comments.length} Comment{this.state.comments.length > 1 || this.state.comments.length === 0 ? 's' : null}
                        </Link>

                        <Dialog open={this.state.showCommentsDialog} onClose={() => {
                            this.handleStateChange({showCommentsDialog: false})
                        }}
                                aria-labelledby="form-dialog-title"
                                maxWidth='xs'
                                fullWidth
                        >
                            <DialogTitle id="form-dialog-title">Comments</DialogTitle>
                            <Divider/>
                            <DialogContent>
                                <List>
                                    {
                                        this.state.comments.length > 0 ?
                                            this.state.comments.map((comment, index) => {
                                                return (
                                                    <CommentListItem key={index} comment={comment}
                                                                     removeComment={this.deleteComment}/>
                                                )
                                            }) :
                                            <ListItem>
                                                <Typography variant="body2">
                                                    No comments
                                                </Typography>
                                            </ListItem>
                                    }
                                </List>
                            </DialogContent>
                        </Dialog>
                    </Typography>
                </CardContent>

                <Divider/>

                <CardActions disableSpacing>
                    <Grid
                        container
                        justify="space-between"
                    >
                        <Vote data={this.props.data}/>

                        <Grid
                            item
                        >
                            <IconButton aria-label="comment" title='Comment' onClick={() => {
                                this.handleStateChange({dialog: true})
                            }}>
                                <Comment/>
                            </IconButton>
                        </Grid>
                    </Grid>
                    <Dialog open={this.state.dialog} onClose={() => (this.handleStateChange({dialog: false}))}
                            aria-labelledby="form-dialog-title"
                            maxWidth='sm' fullWidth={true}>
                        <DialogTitle id="form-dialog-title">Comment</DialogTitle>
                        <DialogContent>
                            <TextField
                                autoFocus
                                margin="dense"
                                label="Comment"
                                fullWidth
                                value={this.state.commentText}
                                onChange={event => {
                                    event.preventDefault();
                                    this.handleStateChange({
                                        commentText: event.target.value
                                    });
                                }}
                            />
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={() => (this.handleStateChange({dialog: false}))} color="primary">
                                Cancel
                            </Button>
                            <Button onClick={this.createComment} color="primary">
                                Comment
                            </Button>
                        </DialogActions>
                    </Dialog>

                </CardActions>

            </Card>
        );
    }
}

Post.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Post)
