import { UPDATE_TWEET, TWEET_URL, TOKEN } from './types';
import axios from 'axios';

export default function updateTweet(tweet) {
  return dispatch => {
    axios.put(TWEET_URL,tweet,
      { headers: 
        {
        "api-token": TOKEN,
        'content-type': 'multipart/form-data'
         },
  
      }).then(res => {
    dispatch(updateTweetAsync(tweet));
    })
  }
}

function updateTweetAsync(tweet){
  return {
    type: UPDATE_TWEET,
    payload: tweet
  };
}
