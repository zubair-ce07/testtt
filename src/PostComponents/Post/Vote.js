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
            upvoteCheck: false,
            downvotes: [],
            downvoteCheck: false,
        }
    }

    setVote = (voteType, update = false) => {
        const secondaryVote = voteType === 'upvote' ? 'downvote' : 'upvote';
        const name = voteType + 'Check';
        const secondaryName = secondaryVote + 'Check';
        if (update)
            this.setState({
                [name]: true,
                [secondaryName]: false
            });
        else
        {
            this.setState({
                [name]: !this.state[name],
                [secondaryName]: false
            });
        }
    };

    handleUpvoteClick = () => {
        let data = {
            user: 6
        };
        if (this.state.upvoteCheck) {
            deleteUpvoteDB(this.props.data, 6).then(response => {
                this.setState({
                    upvotes: this.state.upvotes.filter(vote => {
                        return vote.post !== response.data.post && vote.user === 6
                    })
                });
                this.setVote('upvote')
            });
        } else {
            if (this.state.downvoteCheck) {
                this.handleDownvoteClick()
            }
            createUpvoteDB(this.props.data, data).then(response => {
                this.setState(state => {
                    const upvotes = state.upvotes.concat(response.data);
                    return {
                        upvotes: upvotes,
                    }
                });
                this.setVote('upvote')
            });
        }
    };

    handleDownvoteClick = () => {
        let data = {
            user: 6
        };
        if (this.state.downvoteCheck) {
            deleteDownvoteDB(this.props.data, 6).then(response => {
                this.setState({
                    downvotes: this.state.downvotes.filter(vote => {
                        return vote.post !== response.data.post && vote.user === 6
                    })
                });
                this.setVote('downvote')
            });
        } else {
            if (this.state.upvoteCheck) {
                this.handleUpvoteClick()
            }
            createDownvotevoteDB(this.props.data, data).then(response => {
                this.setState(state => {
                    const downvotes = state.downvotes.concat(response.data);
                    return {
                        downvotes: downvotes,
                    }
                });
                this.setVote('downvote')
            });
        }
    };


    fetchUpvotes = () => {
        fetchUpvotesDB(this.props.data).then(response => {
            this.setState({
                upvotes: response.data
            });
            if (this.state.upvotes.filter(vote => vote.user === 6).length > 0)
                this.setVote('upvote', true)
        });
    };

    fetchDownvotes = () => {
        fetchDownVotesDB(this.props.data).then(response => {
            this.setState({
                downvotes: response.data
            });
            if (this.state.downvotes.filter(vote => vote.user === 6).length > 0)
                this.setVote('downvote', true)
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
                    <ArrowUpward color={this.state.upvoteCheck ? 'primary' : 'inherit'}/>
                </IconButton>
                <Link href='/' color='inherit'>
                    {this.state.upvotes.length}
                </Link>
                <IconButton aria-label="downvote" title='Downvote' onClick={this.handleDownvoteClick}>
                    <ArrowDownward color={this.state.downvoteCheck ? 'error' : 'inherit'}/>
                </IconButton>
                <Link href='/' color='inherit'>
                    {this.state.downvotes.length}
                </Link>
            </div>
        )
    }
}

export default Vote;
