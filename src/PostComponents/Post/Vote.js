import React from "react";
import {IconButton, Link} from "@material-ui/core";
import {ArrowDownward, ArrowUpward,} from '@material-ui/icons';
import {
    createDownvotevoteDB,
    createUpvoteDB,
    deleteDownvoteDB,
    deleteUpvoteDB,
    fetchDownVotesDB,
    fetchUpvotesDB
} from "../../APIClient/APIClient";

class Vote extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            upvotes: [],
            upvote_check: false,
            downvotes: [],
            downvote_check: false,
        }
    }


    setUpvote = (update = false) => {
        if (update)
            this.setState({
                upvote_check: true,
                downvote_check: false
            });
        else
            this.setState({
                upvote_check: !this.state.upvote_check,
                downvote_check: false
            });
    };

    handleUpvoteClick = () => {
        let data = {
            'user': 6
        };
        if (this.state.upvote_check) {
            deleteUpvoteDB(this.props.data, 6).then(response => {
                this.setState({
                    upvotes: this.state.upvotes.filter(vote => {
                        return vote.post !== response.data.post && vote.user === 6
                    })
                });
                this.setUpvote()
            });
        } else {
            if (this.state.downvote_check) {
                this.handleDownvoteClick()
            }
            createUpvoteDB(this.props.data, data).then(response => {
                this.setState(state => {
                    const upvotes = state.upvotes.concat(response.data);
                    return {
                        upvotes: upvotes,
                    }
                });
                this.setUpvote()
            });
        }
    };

    setDownvote = (update = false) => {
        if (update)
            this.setState({
                downvote_check: true,
                upvote_check: false
            });
        else
            this.setState({
                downvote_check: !this.state.downvote_check,
                upvote_check: false
            });
    };

    handleDownvoteClick = () => {
        let data = {
            'user': 6
        };
        if (this.state.downvote_check) {
            deleteDownvoteDB(this.props.data, 6).then(response => {
                this.setState({
                    downvotes: this.state.downvotes.filter(vote => {
                        return vote.post !== response.data.post && vote.user === 6
                    })
                });
                this.setDownvote()
            });
        } else {
            if (this.state.upvote_check) {
                this.handleUpvoteClick()
            }
            createDownvotevoteDB(this.props.data, data).then(response => {
                this.setState(state => {
                    const downvotes = state.downvotes.concat(response.data);
                    return {
                        downvotes: downvotes,
                    }
                });
                this.setDownvote()
            });
        }
    };


    fetchUpvotes = () => {
        fetchUpvotesDB(this.props.data).then(response => {
            this.setState({
                upvotes: response.data
            });
            if (this.state.upvotes.filter(vote => vote.user === 6).length > 0)
                this.setUpvote(true)
        });
    };

    fetchDownvotes = () => {
        fetchDownVotesDB(this.props.data).then(response => {
            this.setState({
                downvotes: response.data
            });
            if (this.state.downvotes.filter(vote => vote.user === 6).length > 0)
                this.setDownvote(true)
        });
    };

    componentDidMount() {
        this.fetchUpvotes();
        this.fetchDownvotes();
        setInterval(() => {
            this.fetchUpvotes();
            this.fetchDownvotes();
        }, 5000);
    }

    componentWillUnmount() {
        clearInterval();
    }

    render() {
        return (
            <div>
                <IconButton aria-label="upvote" title='Upvote' onClick={this.handleUpvoteClick}>
                    <ArrowUpward color={this.state.upvote_check ? 'primary' : 'inherit'}/>
                </IconButton>
                <Link href='/' color='inherit'>
                    {this.state.upvotes.length}
                </Link>
                <IconButton aria-label="downvote" title='Downvote' onClick={this.handleDownvoteClick}>
                    <ArrowDownward color={this.state.downvote_check ? 'error' : 'inherit'}/>
                </IconButton>
                <Link href='/' color='inherit'>
                    {this.state.downvotes.length}
                </Link>
            </div>
        )
    }
}

export default Vote;
