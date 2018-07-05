import React from 'react';

export const Note = (props) => {
  return (
    <div>
      <div className="card-body">
        {props.edit
          ? <textarea
              onChange={props.handleTextChange}
              className="form-input"
              value={props.content}
              rows="6" />
          : <p>{props.text}</p>}
      </div>
      <div className="card-footer btn-right">
        {props.edit
          ? <SaveButton updateTweet={props.updateTweet} />
          : <EditButton toggleEdit={props.toggleEdit} />}
      </div>
    </div>
  );
}

const EditButton = (props) => {
  return (
    <button
      onClick={props.toggleEdit}
      className="btn btn-link">
      Edit
    </button>
  );
}

const SaveButton = (props) => {
  return (
    <button
      onClick={props.updateTweet}
      className="btn btn-primary">
      Save
    </button>
  );
}
