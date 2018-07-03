import React, { Component } from 'react';
import {connect} from 'react-redux';

class RewardList extends Component {
  renderRewards() {
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
        {this.renderRewards()}
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

export default connect(mapStateToProps, null)(RewardList);
