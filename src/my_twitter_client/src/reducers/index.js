import { combineReducers } from 'redux';
import recentTweetsReducer from './reducer_wanted_list';
import ToastReducer from './reducer_toast';

const rootReducer = combineReducers({
  recentTweets: recentTweetsReducer,
  toast: ToastReducer
});

export default rootReducer;
