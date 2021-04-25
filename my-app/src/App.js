import React, { Component } from 'react';
import './App.css'
import LoginPage from './components/LoginPage'
import SearchCriteriaPage from './components/SearchCriteriaPage'
import SearchingPage from './components/SearchingPage';
import HomePage from './components/HomePage'
import SettingsPage from './components/SettingsPage'
import ContactUsPage from './components/ContactUsPage'
import LoginAuthenticate from './components/LoginAuthenticate'
import AdminSettingsPage from './components/AdminSettingsPage';
import SettingsAuthenticate from './components/SettingsAuthenticate';
import RegisterAccount from './components/RegisterAccount';
import RegisterAccountConfirm from './components/RegisterAccountConfirm';


// Imports from react-router
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect
} from "react-router-dom";

export default class App extends Component {
  constructor(props){
      super(props);
      this.state = {
          email: '',
          password: '',
          isAuthenticated: '/LoginPage',
          platformSelector: 'Select',
          hashTags: '',
          locations: '',
          phrases: '',
          startDate: '',
          endDate: '',
          fetchURL: '',
          userAdmin: true,
          isHidden: false
      };

      this.handleLogin = this.handleLogin.bind(this);
      this.handleLogout = this.handleLogout.bind(this);
      this.handleEmailChange = this.handleEmailChange.bind(this);
      this.handlePasswordChange = this.handlePasswordChange.bind(this);
      this.handleHashTagsInput = this.handleHashTagsInput.bind(this);
      this.handleLocationsInput = this.handleLocationsInput.bind(this);
      this.handlePhrasesInput = this.handlePhrasesInput.bind(this);
      this.handleStartDateInput = this.handleStartDateInput.bind(this);
      this.handleEndDateInput = this.handleEndDateInput.bind(this);
      this.handleSearch = this.handleSearch.bind(this);
      this.handleSelection = this.handleSelection.bind(this);
    }
  
  handleLogin(event){
    const fetchUrl = '/api/authenticateLogin';
        const fetchBody = {
            method: 'POST',
            body: JSON.stringify({
                email: this.state.email,
                password: this.state.password
            })
        }
        fetch(fetchUrl, fetchBody)
            .then(response => response.json())
            .then(data => {
              if (data.result == "OK Email/Password Validated"){
                this.setState({isAuthenticated: '/HomePage'})
              }
            }) 
        
        this.getUserType()
  }
  getUserType(){
    const fetchURL = '/api/getAccount';
    const fetchBody = {
      method: 'POST',
      body: JSON.stringify({
        email: this.state.email
      })
    }

    fetch(fetchURL, fetchBody)
      .then(response => response.json())
      .then(data => {
          this.setState({
            userAdmin: data.b_admin
          })
        }
      )
  }

  getAuth(){
    return this.state.isAuthenticated;
  }
  
  handleEmailChange(event){
    this.setState({email: event.target.value});
  }

  handlePasswordChange(event){
    this.setState({password: event.target.value});
  }

  handleSelection(newPlatform){
    this.setState({platformSelector: newPlatform.target.value});
    if(newPlatform.target.value == "Twitter"){
        this.setState({
          fetchURL: '/api/scrapeTwitter',
          isHidden: false
        });
        
    }
    else if(newPlatform.target.value == "Instagram"){
        this.setState({
          fetchURL: '/api/scrapeInstagram',
          isHidden: true
        });
    }
    else {
      this.setState({
        isHidden: false
      })
    }
  }
  handleHashTagsInput(newHashTags){
      this.setState({hashTags: newHashTags});
  }
  handleLocationsInput(newLocations){
      this.setState({locations: newLocations});
  }
  handlePhrasesInput(newPhrases){
      this.setState({phrases: newPhrases});
  }
  handleStartDateInput(newStartDate){
      this.setState({startDate: newStartDate});
  }
  handleEndDateInput(newEndDate){
      this.setState({endDate: newEndDate});
  }

  async handleSearch(event){
  //Handles search POST function
  //If Twitter Platform selected, POST Twitter info
  //Else Instagram Platform selected, POST Instagram info

      if (this.state.platformSelector == 'Twitter'){
          fetch(this.state.fetchURL, {
              method: 'POST',
              body: JSON.stringify({
                  email: this.state.email,
                  hashTags: this.state.hashTags,
                  locations: this.state.locations,
                  phrases: this.state.phrases,
                  earliestDate: this.state.startDate,
                  latestDate: this.state.endDate
              })
          })
          .then(res => res.blob())
          .then(blob => {
            const url = URL.createObjectURL(blob)
            document.location = url
          }) 
      }
      else if(this.state.hashTags != ""){
        fetch(this.state.fetchURL, {
            method: 'POST',
            body: JSON.stringify({
              email: this.state.email,
              search_term: this.state.hashTags,
              search_category: "hashtag"
          })
        })
        .then(res => res.blob())
        .then(blob => {
          const url = URL.createObjectURL(blob)
          document.location = url
        })          
      }
      else if(this.state.locations != ""){
        fetch(this.state.fetchURL, {
          method: 'POST',
          body: JSON.stringify({
            email: this.state.email,
            search_term: this.state.locations,
            search_category: "location"
          })
        })
        .then(res => res.blob())
        .then(blob => {
          const url = URL.createObjectURL(blob)
          document.location = url
        }) 
      }

}


  sendUser(){
    const fetchURL = '/api/getAccount';

    fetch(fetchURL, {
      method: 'POST',
      body: JSON.stringify({
          email: this.state.email
      })
  })
  .then(results => results.json())
  .then(data => {
    return data.s_first + " " + data.s_last;
  })
  }
  sendHashTags(){
    if (this.state.hashTags !== ""){
      return this.state.hashTags;
    }

    return 'N/A';
  }
  sendLocations(){
    if (this.state.locations !== ""){
      return this.state.locations;
    }

    return 'N/A';
  }
  sendPhrases(){
    if (this.state.phrases !== ""){
      return this.state.phrases;
    }

    return 'N/A';
  }
  sendStartDate(){
    if (this.state.startDate !== ""){
      return this.state.startDate;
    }

    return 'N/A';
  }
  sendEndDate(){
    if (this.state.endDate !== ""){
      return this.state.endDate;
    }

    return 'N/A';
  }
  handleLogout(){
    this.setState({
      email: '',
      password: ''
    })
  }
  componentDidMount(){
    this.setState({
      email: '',
      password: ''
    })
  }

  render(){
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route exact path = '/LoginPage'>
            <LoginPage 
              title = 'Log In' 
              email = {this.state.email} 
              password = {this.state.password} 
              handleEmailChange = {this.handleEmailChange} 
              handlePasswordChange = {this.handlePasswordChange} 
              handleLogin = {this.handleLogin} 
              handleLogout = {this.handleLogout}
            />
          </Route>
          <Route exact path = '/RegisterAccount'>
            <RegisterAccount title = 'Register Account' />
          </Route>
          <Route exact path = '/RegisterAccountConfirm'>
            <RegisterAccountConfirm title = 'Register Account Confirm' />
          </Route>
          <Route exact path = '/HomePage'>
            <HomePage 
              title = 'HomePage' 
              email = {this.state.email}
            />
          </Route>
          <Route exact path = '/SearchCriteriaPage'>
            <SearchCriteriaPage 
              title = 'Search Criteria'
              email = {this.state.email}
              platformSelector = {this.state.platformSelector}
              hashTags = {this.state.hashTags}
              locations = {this.state.locations}
              phrases = {this.state.phrases}
              startDate = {this.state.startDate}
              endDate = {this.state.endDate}
              handleSelection = {this.handleSelection}
              handleHashTagsInput = {this.handleHashTagsInput}
              handleLocationsInput = {this.handleLocationsInput}
              handlePhrasesInput = {this.handlePhrasesInput}
              handleStartDateInput = {this.handleStartDateInput}
              handleEndDateInput = {this.handleEndDateInput}
              handleSearch = {this.handleSearch}
              hideComponent = {this.state.isHidden}
            />
          </Route>
          <Route exact path = '/SearchingPage'>
            <SearchingPage 
              title = 'Searching'
              email = { this.state.email }
              user = { this.sendUser }
              hashTags = { this.state.hashTags }
              locations = { this.sendLocations() }
              phrases = { this.sendPhrases() }
            />
          </Route>
          <Route exact path = '/SettingsPage'>
            <SettingsPage 
              title = 'Settings'
              email = {this.state.email} 
            />
          </Route>
          <Route exact path = '/AdminSettingsPage'>
            <AdminSettingsPage
              title = 'Admin Settings'
              email = {this.state.email}
             />
            <Route exact path = '/SettingsAuthenticate'>
              <SettingsAuthenticate
                userAdmin = {this.state.userAdmin}
              />
            </Route>
          </Route>
          <Route exact path = '/ContactUsPage'>
            <ContactUsPage title='Contact Us'></ContactUsPage>
          </Route>
          <Route exact path = '/LoginAuthenticate'>
            <LoginAuthenticate 
              isAuthenticated={this.state.isAuthenticated}
              email = {this.state.email}
              password = {this.state.password}
              getAuth = {this.getAuth()}
              redirect = {<div><Redirect to={this.state.isAuthenticated}></Redirect></div>}
            />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}
}
