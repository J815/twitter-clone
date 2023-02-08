import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { ProfileDisplayElement } from './profiles/profiledetail'
import { FeedElement, TweetElement, TweetDetailElement } from './tweets/parts';
import reportWebVitals from './reportWebVitals';

const appElement= document.getElementById('root')
if(appElement){   
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  appElement
);
}
const e=React.createElement

const tweeterElement= document.getElementById('tweeter')
if(tweeterElement){  
  ReactDOM.render(
    e(TweetElement, tweeterElement.dataset),
    tweeterElement
    );
}
const tweeterElementFeed= document.getElementById('tweeter-feed')
if(tweeterElementFeed){  
  ReactDOM.render(
    e(FeedElement, tweeterElementFeed.dataset),
    tweeterElementFeed
    );
}
const tweeterDetailElement= document.querySelectorAll(".tweeter-detail") 
tweeterDetailElement.forEach(container=> {
    ReactDOM.render(
      e(TweetDetailElement, container.dataset),
      container);
  })
const userProfileDetailElement= document.querySelectorAll(".profile-detail") 
userProfileDetailElement.forEach(container=> {
      ReactDOM.render(
        e(ProfileDisplayElement, container.dataset),
        container);
    })
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
