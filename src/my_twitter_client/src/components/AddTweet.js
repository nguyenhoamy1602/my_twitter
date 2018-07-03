import React, { Component } from 'react';

class AddTweet extends Component {
  render() {
    return (
      <div className={`modal ${this.props.open ? 'active' : null}`}>
        <div className="modal-overlay"></div>
        <div className="modal-container">
          <div className="modal-header">
            <button
              onClick={this.props.close}
              className="btn btn-clear float-right"></button>
            <div className="modal-title">
              <h4>Add a Tweet</h4>
            </div>
          </div>
          <div className="modal-body">
            <div className="content">
              <form>
                <div className="form-group">
                  <label className="form-label">What's on your mind?</label>
                  <input
                    value={this.props.newTweet}
                    onChange={this.props.onNewTweet}
                    className="form-input"
                    type="text"
                    placeholder="It's a beautiful day and I'm lying in bed" />
                </div>
                <div className="form-group">
                  <label className="form-label">Attached an image!</label>
                  <input
                    value={this.props.newImage}
                    onChange={this.props.onNewImage}
                    className="form-input"
                    type="file"
                    placeholder="image.jpg" />
                </div>


              </form>
            </div>
          </div>
          <div className="modal-footer">
            <button
              onClick={this.props.createTweet}
              className="btn btn-primary">Save</button>
          </div>
        </div>
      </div>
    );
  }
}

export default AddTweet;
