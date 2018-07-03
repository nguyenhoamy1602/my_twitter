import { GET_WANTED_LIST } from './types';
import axios from 'axios';


var token = "eyJhbGciOiJIUzI1NiIsImlhdCI6MTUzMDUxMDIzMywiZXhwIjoxNTMxNzE5ODMzfQ.eyJpZCI6IlVzZXI6MSIsIm5hbWUiOiJOZ3V5ZW4gSG9hIE15In0.Ly_7n37O4F-E-Khtku567Roj8PadP4LwuXCIymiLyds";
export const URL = "http://localhost:5000/api";

export default function getWantedList() {
  return dispatch => {
    axios.get(URL + '/tweet/',
  { headers: {
    "api-token": token
  }})
      // axios.get(URL + '/tweet')
      .then(res => {
        console.log('Wanted list ::', res.data);
        const people = res.data.map(tweet => {
          return tweet;
        });
        dispatch(getWantedListAsync(people));
      });
  }
}

function getWantedListAsync(people){
  return {
    type: GET_WANTED_LIST,
    payload: people
  };
}


