import { GET_TWEET_LIST,
         ADD_TWEET,
         UPDATE_TWEET,
         DELETE_TWEET } from '../actions/types';

export default function(state=[], action) {

  switch (action.type) {
    case GET_TWEET_LIST:
      return action.payload;

    case ADD_TWEET:
      return [action.payload, ...state];

    case UPDATE_TWEET:
      return state.map(tweet => {
        if(tweet.id === action.payload.id) {
          return action.payload;
        }
        return tweet;
      });

    case DELETE_TWEET:
      return state.filter(tweet => tweet.id !== action.payload);

    default:
      return state;
  }

}
