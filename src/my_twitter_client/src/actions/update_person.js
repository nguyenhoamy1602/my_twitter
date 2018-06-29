import { UPDATE_PERSON } from './types';

export default function updatePerson(tweet) {
  return dispatch => {
    dispatch(updatePersonAsync(tweet));
  }
}

function updatePersonAsync(tweet){
  return {
    type: UPDATE_PERSON,
    payload: tweet
  };
}
