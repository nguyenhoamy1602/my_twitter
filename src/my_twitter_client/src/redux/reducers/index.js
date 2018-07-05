import { combineReducers } from 'redux';
import recentTweetsReducer from './reducer_tweet_list';
import ToastReducer from './reducer_toast';
import authReducer from './reducer_auth';

const rootReducer = combineReducers({
  recentTweets: recentTweetsReducer,
  toast: ToastReducer,
  auth: authReducer,
});

export default rootReducer;
