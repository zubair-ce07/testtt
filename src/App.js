import React from 'react';
import ReactDOM from 'react-dom';

import {
  MDBContainer,
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarNav,
  MDBNavbarToggler,
  MDBCollapse,
  MDBNavItem,
  MDBNavLink,
  MDBFormInline
} from "mdbreact";

import { BrowserRouter as Router } from "react-router-dom";

const categories = ["World", "Business", "Tech", "Sport"];

class Homepage extends React.Component {
  constructor() {
    super();
    this.state = {
      items: [],
      isOpen: false
    };
    this.onClick = this.onClick.bind(this);
  }

  componentDidMount() {
    // this.getItems();
  }

  getItems() {
    fetch("http://127.0.0.1")
      .then(results => results.json())
      .then(results => this.setState({ items: results }));
  }

  onClick() {
    this.setState({
      collapse: !this.state.collapse
    });
  }

  render() {
    const bgIndigo = { backgroundColor: "rgb(234, 234, 234)" };
    const text_color = { color: "grey" };
    const container = { height: 1300 };
    return (
      <div>
        <Router>
          <header>
            <MDBNavbar style={bgIndigo} dark expand="md" scrolling fixed="top">
              <MDBNavbarBrand href="/">
                <strong style={text_color}>Social App</strong>
              </MDBNavbarBrand>
              <MDBNavbarToggler onClick={this.onClick} />
              <MDBCollapse isOpen={this.state.collapse} navbar>
                <MDBNavbarNav left>
                  <MDBNavItem active>
                    <MDBNavLink to="#">Home</MDBNavLink>
                  </MDBNavItem>
                </MDBNavbarNav>
                <MDBNavbarNav right>
                  <MDBNavItem>
                    <MDBFormInline waves>
                      <div className="md-form my-0">
                        <Filter onFilter={this.handleFilter} />
                      </div>
                    </MDBFormInline>
                  </MDBNavItem>
                </MDBNavbarNav>
              </MDBCollapse>
            </MDBNavbar>
          </header>
        </Router>
        <MDBContainer style={container} className="text-center mt-5 pt-5">
          <div className="homepage">
            <Feed />
          </div>
        </MDBContainer>
      </div>
    );
  }
}

class Feed extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: JSON.parse(localStorage.getItem("posts")) || [],
      filteredPosts: []
    };

    this.handleNewPost = this.handleNewPost.bind(this);
    this.handleFilter = this.handleFilter.bind(this);
  }

  handleNewPost(post) {
    var posts = this.state.posts.concat([post]);
    this.setState({
      posts: posts
    });
    localStorage.setItem("posts", JSON.stringify(posts));
  }

  handleFilter(filter) {
    this.setState({
      filteredPosts: this.state.posts.filter(
        post =>
          post.category.toUpperCase() === filter.toUpperCase() ||
          post.content.includes(filter)
      )
    });
  }

  render() {
    const posts = this.state.posts.map((post, index) => (
      <Post key={index} value={post} />
    ));
    const filteredPosts = this.state.filteredPosts.map((post, index) => (
      <Post key={index} value={post} />
    ));
    return (
      <div className="feed">
        <PostForm onSubmit={this.handleNewPost} />
        {filteredPosts.length > 0 ? filteredPosts : posts}
      </div>
    );
  }
}

class Post extends React.Component {
  render() {
    return (
      <div
        className=" card"
        style={{ display: "inline-block", margin: "5px", padding: 0 }}
      >
        <div style={{ background: "rgb(241, 241, 241)", padding: "10px" }}>
          <img
            src="data:image/png;base64,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"
            style={{
              borderRadius: "50%",
              border: "1px solid grey",
              height: "40px"
            }}
          />
          <div
            style={{
              display: "inline-block",
              marginLeft: "10px",
              verticalAlign: "middle"
            }}
          >
            <h6 style={{ margin: "0px" }}>Poster name </h6>
            <small>posted on </small>
          </div>
        </div>
        <div className="content" style={{ padding: "10px" }}>
          <p>This is post content </p>
          <img
            src="http://www.seriouswheels.com/pics-2009/a/2009-Audi-Sportback-Concept-Front-Lights-Black-2-1920x1440.jpg"
            alt="Image to be here"
            style={{ maxWidth: "100%" }}
          />
        </div>
        <hr />
        <div
          style={{
            display: "inline-block",
            width: "100%",
            verticalAlign: "middle",
            margin: "2px 5px"
          }}
        >
          <button
            className="btn btn-success btn-sm"
            style={{
              width: "80px",
              textAlign: "center",
              border: "1px solid rgb(241, 2241, 241)"
            }}
          >
            <i className="fas fa-arrow-up" /> Up
          </button>
          <small
            style={{
              margin: "10px",
              width: "100%",
              color: "grey",
              height: "100%",
              verticalAlign: "middle"
            }}
          >
            X{" "}
          </small>
          <button
            className="btn btn-danger btn-sm"
            style={{ width: "80px", textAlign: "center" }}
          >
            <span className="fa fa-arrow-down" aria-hidden="true" /> Down
          </button>
          <small
            style={{
              margin: "10px",
              width: "100%",
              color: "grey",
              height: "100%",
              display: "block"
            }}
          >
            X Comments
          </small>
        </div>
      </div>
    );
  }
}

class PostForm extends React.Component {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    this.props.onSubmit({
      category: this.category.value,
      content: this.content.value
    });
    this.category.value = categories[0];
    this.content.value = "";
    event.preventDefault();
  }

  render() {
    return (
      <div className="post-form" class="card form-group">
        <form onSubmit={this.handleSubmit}>
          <textarea class="form-control"  style={{ margin: '5px' }} type="text" rows="4" ref={input => (this.content = input)} placeholder="Whats on your mind.." />
          <hr />
          <button class="btn btn-primary float-right" style={{ margin: '5px' }}>Add post</button>
        </form>
      </div>
    );
  }
}

class Filter extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: "" };

    this.handleChange = this.handleChange.bind(this);
    this.handleKeyUp = this.handleKeyUp.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
    if (event.target.value === "") {
      this.props.onFilter("");
    }
  }

  handleKeyUp(event) {
    if (event.key === "Enter") {
      this.props.onFilter(this.state.value);
    }
  }

  render() {
    return (
      <div>
        <label>
          <MDBFormInline waves>
            <div className="md-form my-0">
              <input
                type="search"
                value={this.state.value}
                onChange={this.handleChange}
                onKeyUp={this.handleKeyUp}
                placeholder="Filter"
              />
            </div>
          </MDBFormInline>
        </label>
      </div>
    );
  }
}
