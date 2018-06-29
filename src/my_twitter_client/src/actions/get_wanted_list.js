import { GET_WANTED_LIST } from './types';
import axios from 'axios';

export default function getWantedList() {
  return dispatch => {
    axios.get('http://localhost:5000/tweet')
      .then(res => {
        console.log('Wanted list ::', res.data);
        const people = res.data.map(person => {
          person.note = 'none';
          person.image = "https://api.adorable.io/avatars/face/eyes3/nose2/mouth4/F5CDE6"
          return person;
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
