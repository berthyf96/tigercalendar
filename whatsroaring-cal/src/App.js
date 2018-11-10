import React, { Component } from 'react';
import './App.css';

import Calendar from './Calendar'

class App extends Component {
  render() {
    return (
      <div className="app">
        <div className="jumbotron">
          <div>
            <h1>
              WhatsRoaring
            </h1>
            <p>Here's what's roaring around Princeton.</p>
          </div>
        </div>
        <Calendar />
      </div>
      
    );
  }
}

export default App;
