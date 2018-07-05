
import React, { Component } from 'react';
import { Route, BrowserRouter, Switch} from 'react-router-dom'
import SignIn from './components/SignIn';

export default class App extends Component {
  render() {
    return(
        <BrowserRouter>
          <div>
            <Switch>
              {/* <Route path='/login' component={Login} />
              <Route path='/signup' component={Signup} /> */}
              <Route path='/signin' component={SignIn} />
              <Route render={() => <h3>No Match</h3>} />
            </Switch>
          </div>
        </BrowserRouter>)
  }
}