import React, { Component } from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import addTweet from '../redux/actions/add_tweet';
import getTweetList from '../redux/actions/get_tweet_list';
import clearToast from '../redux/actions/clear_toast';
import TweetCard from './TweetCard';
import UserList from './UserList';
import AddTweet from './AddTweet';
import SignIn from './SignIn';
import Toast from './Toast';
import LoadingSpinner from './LoadingSpinner';
import {signIn, logOut} from '../redux/actions/sign_in';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      newTweet: '',
      newImage: null
    }
    this.toggleModalState = this.toggleModalState.bind(this);
    this.toggleLoginState = this.toggleLoginState.bind(this);
    this.handleNewTweetChange = this.handleNewTweetChange.bind(this);
    this.handleNewImage = this.handleNewImage.bind(this);
    this.handleLogin = this.handleLogin.bind(this);
    this.handleLogout = this.handleLogout.bind(this);
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
  
  toggleLoginState() {
    if(this.state.openLogin) {
      this.clearFormAndCloseLogin();
    } else {
      this.setState({
        openLogin: true
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
  
  clearFormAndCloseLogin() {
    this.setState({
      openLogin: false
    });
  }
  
  handleTweetCreation() {
    const tweet = new FormData();
    tweet.append('image', this.state.newImage)
    tweet.append('text', this.state.newTweet)
    this.props.addTweet(tweet);
    this.clearFormAndCloseModal();
  }

  handleLogin(response) {
    this.props.signIn(response);
    this.clearFormAndCloseLogin();
  }

  handleLogout() {
    this.props.logOut();
  }

  handleClearToast() {
    this.props.clearToast();
  }

  renderLoginButton() {
    if (this.props.auth.isAuthenticated) {
        return (<button
        className="btn btn-right"
        onClick={this.handleLogout}> Log Out
        </button>
        );
    } else {
      return (<button
        className="btn btn-right"
        onClick={this.toggleLoginState}> Sign In
        </button>
        );
    }
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
        {this.props.auth.isAuthenticated ? <button
        className="btn btn-right"
        onClick={this.toggleModalState}>Post a Tweet</button>
        : null}
        </h2>
        
        {this.renderUsers()}
        </div>
        <div className="column col-md-6">
        {this.renderLoginButton()}
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
        
        <SignIn
        logIn={this.handleLogin}
        open={this.state.openLogin}
        close={this.toggleLoginState}
        isAuthenticated={this.props.auth.isAuthenticated}
        logOut={this.handleLogout}/>
        </div>
      );
    }
  }

  //connects root reducer to props
  function mapStateToProps(state) {
    return {
      recentTweets: state.recentTweets,
      toast: state.toast,
      auth: state.auth
    }
  }
  
  //connects redux actions to props
  function mapDispatchToProps(dispatch) {
    return bindActionCreators({
      getTweetList: getTweetList,
      addTweet: addTweet,
      clearToast: clearToast,
      signIn: signIn,
      logOut: logOut
    }, dispatch);
  }
  
  export default connect(mapStateToProps, mapDispatchToProps)(App);
  