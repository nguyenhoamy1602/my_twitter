import React, { Component } from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import addTweet from '../actions/add_tweet';
import getTweetList from '../actions/get_tweet_list';
import clearToast from '../actions/clear_toast';
import TweetCard from './TweetCard';
import UserList from './UserList';
import AddTweet from './AddTweet';
import Toast from './Toast';
import LoadingSpinner from './LoadingSpinner';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      newTweet: '',
      newImage: null
    }
    this.toggleModalState = this.toggleModalState.bind(this);
    this.handleNewTweetChange = this.handleNewTweetChange.bind(this);
    this.handleNewImage = this.handleNewImage.bind(this);
    this.handleTweetCreation = this.handleTweetCreation.bind(this);
    this.handleClearToast = this.handleClearToast.bind(this);
  }
  componentDidMount() {
    this.props.getTweetList();
  }
  renderUsers() {
    if(this.props.recentTweets) {
      return this.props.recentTweets.map(tweet => {
        return <TweetCard key={tweet.name} tweet={tweet} />;
      });
    } else {
      return <LoadingSpinner />;
    }
  }
  toggleModalState() {
    if(this.state.openModal) {
      this.clearFormAndCloseModal();
    } else {
      this.setState({
        openModal: true
      })
    }
  }
  handleNewTweetChange(e) {
    this.setState({
      newTweet: e.target.value
    });
  }
  handleNewImage(e) {
    this.setState({
      newImage: e.target.files[0]
    });
  }
  clearFormAndCloseModal() {
    this.setState({
      newTweet: '',
      openModal: false
    });
  }
  handleTweetCreation() {
    const tweet = new FormData();
    tweet.append('image', this.state.newImage)
    tweet.append('text', this.state.newTweet)
    this.props.addTweet(tweet);
    this.clearFormAndCloseModal();
  }
  handleClearToast() {
    this.props.clearToast();
  }
  render() {
    return (
      <div className="App container">
        {this.props.toast
        ? <Toast
            dismiss={this.handleClearToast}
            message={this.props.toast} />
        : null}
        <div className="card-container">
          <div className="columns">
            <div className="column col-md-6">
                <h2>
                  Recent Tweets:
                  <button
                    className="btn btn-primary"
                    onClick={this.toggleModalState}>Add</button>
                </h2>

              {this.renderUsers()}
            </div>
            <div className="column col-md-6">
              <UserList />
            </div>
          </div>
        </div>
        <AddTweet
          createTweet={this.handleTweetCreation}
          addToTweetList={this.handleTweetCreation}
          onNewTweet={this.handleNewTweetChange}
          onNewImage={this.handleNewImage}
          text={this.state.newTweet}
          open={this.state.openModal}
          close={this.toggleModalState}/>
      </div>
    );
  }
}

//connects root reducer to props
function mapStateToProps(state) {
  return {
    recentTweets: state.recentTweets,
    toast: state.toast
  }
}

//connects redux actions to props
function mapDispatchToProps(dispatch) {
  return bindActionCreators({
    getTweetList: getTweetList,
    addTweet: addTweet,
    clearToast: clearToast
  }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
