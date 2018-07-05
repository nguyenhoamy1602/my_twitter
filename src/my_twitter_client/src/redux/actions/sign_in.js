import axios from 'axios';
import { AUTH_URL, SET_CURRENT_USER, LOG_OUT_USER } from './types';


export function signIn(profileObj) {
  return dispatch => {
    axios.post(AUTH_URL, profileObj)
      .then(res => {
        dispatch(getTokenAsync(res.data))
      });
  }
}

function getTokenAsync(response) {
  return dispatch => {
    localStorage.setItem('api-token', response.token);
    setAuthorizationToken(response.token);
    console.log(response);
    dispatch(setCurrentUser(response.user));
  }

}


export function setAuthorizationToken(token) {
  if (token) {
    axios.defaults.headers.common['api-token'] = `${token}`;
  } else {
    delete axios.defaults.headers.common['api-token'];
  }
}

export function logOut() {
  return dispatch => {
    localStorage.removeItem('api-token');
    setAuthorizationToken(false);
    dispatch(logOutUser());
  }
}

function setCurrentUser(user) {
  return {
    type: SET_CURRENT_USER,
    user
  };
}

function logOutUser() {
  return {
    type: LOG_OUT_USER,
  }
}