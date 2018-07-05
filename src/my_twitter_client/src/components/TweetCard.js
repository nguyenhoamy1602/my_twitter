import React, { Component } from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import updateTweet from '../redux/actions/update_tweet';
import deleteTweet from '../redux/actions/delete_tweet';
import { Note } from './Note';

class TweetCard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      editText: false,
      text: props.tweet.text,
      image: props.tweet.image
    };
    this.toggleEdit = this.toggleEdit.bind(this);
    this.handleTextChange = this.handleTextChange.bind(this);
    this.handleUpdateTweet = this.handleUpdateTweet.bind(this);
    this.handleDeleteTweet = this.handleDeleteTweet.bind(this);
  }
  toggleEdit() {
    this.setState({
      editText: !this.state.editText
    })
  }
  handleTextChange(e) {
    this.setState({
      text: e.target.value
    });
  }
  handleUpdateTweet() {
    const tweet = new FormData();
    tweet.append('id', this.props.tweet.id)
    tweet.append('text', this.state.text)
    this.props.updateTweet(tweet);
    this.toggleEdit();
  }
  handleDeleteTweet() {
    this.props.deleteTweet(this.props.tweet);
  }


  renderTweetImage() {
    if (this.props.tweet.image === null) {
      return null;
    } else {
      const title = `Image of ${this.props.tweet.id}`;
      return (
        <div className="card-image">
            <img alt={title} src={this.props.tweet.image} />
        </div>
      );
    }
  }

  render() {
    const tweet = this.props.tweet;
    return (
      <div className="card">
      {this.props.auth.isAuthenticated && this.props.auth.user.name == this.props.tweet.user ?
        <button
          className="btn btn-clear tooltip"
          data-tooltip="Delete because tweet has been captured."
          onClick={this.handleDeleteTweet}></button> : null}
        <div className="card-header">
          <figure
            className="avatar avatar-xl tooltip" data-tooltip={tweet.user}>
            <img alt={tweet.user} src={tweet.userImage} />
          </figure>
          <h4 className="card-title">{tweet.user}</h4>
        </div>
        {this.props.auth.isAuthenticated && this.props.auth.user.name == this.props.tweet.user ?
        <Note
          toggleEdit={this.toggleEdit}
          updateTweet={this.handleUpdateTweet}
          edit={this.state.editText}
          handleTextChange={this.handleTextChange}
          content={this.state.text}
          text={tweet.text}/> : <div>{tweet.text}</div>}
          {this.renderTweetImage()}
          <small className="date">
            <span>Date: </span> {tweet.date}
          </small>
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    auth: state.auth
  }
}

//connects redux actions to props
function mapDispatchToProps(dispatch) {
  return bindActionCreators({
    updateTweet: updateTweet,
    deleteTweet: deleteTweet
  }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(TweetCard);
