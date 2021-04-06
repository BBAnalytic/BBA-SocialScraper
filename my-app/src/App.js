import React from 'react';
import './App.css'
import LoginPage from './components/LoginPage'
import SearchCriteriaPage from './components/SearchCriteriaPage'
import SearchingPage from './components/SearchingPage';
import HomePage from './components/HomePage'
import SettingsPage from './components/SettingsPage'
import ContactUsPage from './components/ContactUsPage'
import RegisterAccount from './components/RegisterAccount'
//Test

// Imports from react-router
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import NavButtons from './components/NavButtons';

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route exact path = '/LoginPage'>
            <LoginPage title = 'Log In' />
          </Route>
          <Route exact path = '/HomePage'>
            <HomePage title = 'HomePage' />
          </Route>
          <Route exact path = '/SearchCriteriaPage'>
            <SearchCriteriaPage title = 'Search Criteria' />
          </Route>
          <Route exact path = '/SearchingPage'>
            <SearchingPage title = 'Searching' />
          </Route>
          <Route exact path = '/SettingsPage'>
            <SettingsPage title = 'Settings' />
          </Route>
          <Route exact path = '/ContactUsPage'>
            <ContactUsPage title='Contact Us'></ContactUsPage>
          </Route>
          <Route exact path = '/RegisterAccount'>
            <RegisterAccount title='Register Account' />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
