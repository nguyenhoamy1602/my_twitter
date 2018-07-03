import { DELETE_TWEET, TWEET_URL, TOKEN } from './types';
import newToast from './new_toast';
import axios from 'axios';

export default function deleteTweet(tweet) {
  const message = `Tweet deleted!`;
  return dispatch => {
    axios.delete(TWEET_URL,
      { headers: 
        {
        "api-token": TOKEN,
         },
         params: { 'id': tweet.id}
  
      }).then(res => {
        dispatch(deleteTweetAsync(tweet.id));
        dispatch(newToast(message));
      })
  }
}

function deleteTweetAsync(tweet){
  return {
    type: DELETE_TWEET,
    payload: tweet // assuming every tweet has a unique name (which you should never do!), this will work.
  };
}
