import { ADD_TWEET, TWEET_URL } from './types';
import newToast from './new_toast';
import axios from 'axios';
import getTweetList from './get_tweet_list';

export default function addTweet(tweet) {
  const message = `You've just added a tweet.`;
  return dispatch => {
    axios.post(TWEET_URL,tweet,
    { headers: 
      {
      'content-type': 'multipart/form-data'
       },

    }).then(res => {
      dispatch(addTweetAsync(res.data));
      dispatch(newToast(message))
    });
  }
}

function addTweetAsync(tweet){
  return {
    type: ADD_TWEET,
    payload: tweet
  };
}