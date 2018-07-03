import { ADD_TWEET, TWEET_URL, TOKEN } from './types';
import newToast from './new_toast';
import axios from 'axios';

export default function addTweet(tweet) {
  const message = `You've just added a tweet.`;
  return dispatch => {
    axios.post(TWEET_URL,tweet,
    { headers: 
      {
      "api-token": TOKEN,
      'content-type': 'multipart/form-data'
       },

    }).then(res => {
      dispatch(addTweetAsync(res.data));
      dispatch(newToast(message))
    })
  }
}

function addTweetAsync(tweet){
  return {
    type: ADD_TWEET,
    payload: tweet
  };
}