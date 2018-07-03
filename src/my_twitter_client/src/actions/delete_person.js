import { DELETE_PERSON } from './types';
import newToast from './new_toast';

export default function deletePerson(tweet) {
  const message = `You've just captured ${tweet.user}. Go collect your user!`;
  return dispatch => {
    dispatch(deletePersonAsync(tweet));
    dispatch(newToast(message))
  }
}

function deletePersonAsync(tweet){
  return {
    type: DELETE_PERSON,
    payload: tweet // assuming every tweet has a unique name (which you should never do!), this will work.
  };
}
