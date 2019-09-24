import React from "react";
import PropTypes from "prop-types";
import {
    Container,
    Box,
    withStyles,
    Typography,
    CircularProgress,
    List,
    Grid
} from "@material-ui/core";

import NewPost from "./NewPost";
import Post from "./Post/Post";
import ListItem from "@material-ui/core/ListItem";
import {createPostDB, deletePostDB, fetchPostsDB} from "../APIClient/APIClient";

const styles = theme => ({
    root: {
        width: 460,
        marginTop: theme.spacing(4),
        marginLeft: 'auto',
        marginRight: 'auto',
        alignItems: 'center',
    },
    newpost: {
        marginBottom: theme.spacing(4)
    },
    post: {
        marginTop: '10px',
        marginBottom: '10px',
        padding: 0
    },
    container: {
        marginTop: theme.spacing(12)
    },
    nopost: {
        color: '#586269',
    }
});

class NewsFeed extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            posts: null
        }
    }

    fetchPosts = () => {
        fetchPostsDB().then(response => {
            this.setState({
                posts: response.data
            });
        })
    };

    addPost = post => {
        createPostDB(post).then(response => {
            this.setState(state => {
                const posts = [response.data].concat(state.posts);
                return {
                    posts
                }
            });
        })
    };

    deletePost = post => {
        deletePostDB(post).then(response => {
            this.setState(state => {
                const posts = state.posts.filter(existing_post => {
                    return post.id !== existing_post.id
                });
                return {
                    posts
                }
            });
        })
    };

    UNSAFE_componentWillMount() {
        setInterval(() => {
            this.fetchPosts();
        }, 5000);
    }

    componentWillUnmount() {
        clearInterval();
    }

    render() {
        const {classes} = this.props;
        return (
            <Container component="main" className={classes.container}>
                <Box className={classes.root}>
                    <NewPost addPost={this.addPost}/>
                    <hr/>
                    <List>
                        {
                            this.state.posts == null ?
                                <Grid
                                    container
                                    justify="center"
                                >
                                    <CircularProgress/>
                                </Grid> :
                                this.state.posts.length > 0 ?
                                    this.state.posts.map(
                                        (data, index) => {
                                            return (
                                                <ListItem key={index} className={classes.post}>
                                                    <Post data={data} removePost={this.deletePost}/>
                                                </ListItem>
                                            )
                                        }
                                    ) :
                                    <ListItem>
                                        <Typography variant={'h6'} className={classes.nopost}>
                                            No posts to display
                                        </Typography>
                                    </ListItem>
                        }
                    </List>
                </Box>
            </Container>
        );
    }
}


NewsFeed.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(NewsFeed)
