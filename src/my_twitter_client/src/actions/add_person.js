import { ADD_PERSON } from './types';
import newToast from './new_toast';

export default function addPerson(tweet) {
  const message = `You've just added ${tweet.user} to the Most Wanted List.`;
  return dispatch => {
    dispatch(addPersonAsync(tweet));
    dispatch(newToast(message))
  }
}

function addPersonAsync(tweet){
  return {
    type: ADD_PERSON,
    payload: tweet
  };
}
