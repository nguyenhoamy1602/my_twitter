import React, { Component } from 'react';
import {connect} from 'react-redux';

class UserList extends Component {
  renderUsers() {
    if(this.props.recentTweets) {
      return this.props.recentTweets.map(r => {
        return (
          <div key={r.user} className="card">
            <div className="card-body">
              <p>{r.user}</p>
            </div>
          </div>
        );
      });
    }
  }
  render() {
    return (
      <div>
        <h2>User List:</h2>
        {this.renderUsers()}
      </div>
    );
  }
}

//connects root reducer to props
function mapStateToProps(state) {
  return {
    recentTweets: state.recentTweets
  }
}

export default connect(mapStateToProps, null)(UserList);
