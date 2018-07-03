import React, { Component } from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import updatePerson from '../actions/update_person';
import deletePerson from '../actions/delete_person';
import { Note } from './Note';

class WantedCard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      editText: false,
      text: props.tweet.text,
      image: props.tweet.image
    };
    this.toggleEdit = this.toggleEdit.bind(this);
    this.handleReasonChange = this.handleReasonChange.bind(this);
    this.handleUpdatePerson = this.handleUpdatePerson.bind(this);
    this.handleDeletePerson = this.handleDeletePerson.bind(this);
  }
  toggleEdit() {
    this.setState({
      editText: !this.state.editText
    })
  }
  handleReasonChange(e) {
    this.setState({
      reason: e.target.value
    });
  }
  handleUpdatePerson() {
    const update = {
      id: this.props.tweet.id,
      image: this.props.tweet.image,
      user: this.props.tweet.user,
      text: this.state.text
    }
    this.props.updatePerson(update);
    this.toggleEdit();
  }
  handleDeletePerson() {
    this.props.deletePerson(this.props.tweet);
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
        <button
          className="btn btn-clear tooltip"
          data-tooltip="Delete because tweet has been captured."
          onClick={this.handleDeletePerson}></button>
        <div className="card-header">
          <figure
            className="avatar avatar-xl tooltip" data-tooltip={tweet.user}>
            <img alt={tweet.user} src={tweet.userImage} />
          </figure>
          <h4 className="card-title">{tweet.user}</h4>
        </div>
        <Note
          toggleEdit={this.toggleEdit}
          updatePerson={this.handleUpdatePerson}
          edit={this.state.editText}
          handleReasonChange={this.handleReasonChange}
          content={this.state.text} />
          {this.renderTweetImage()}
          <small className="date">
            <span>Date: </span> {tweet.date}
          </small>
      </div>
    );
  }
}



//connects redux actions to props
function mapDispatchToProps(dispatch) {
  return bindActionCreators({
    updatePerson: updatePerson,
    deletePerson: deletePerson
  }, dispatch);
}

export default connect(null, mapDispatchToProps)(WantedCard);
