import './App.css';
import Navbar from './components/Navbar';
import Calend from './pages/Calendar.';
import React from "react";
import {
  BrowserRouter as Router,
  Route
} from "react-router-dom";
import Teams from './components/Team';

function App() {
  return (
    <div className="App">
      <Router >
          <Navbar />
          <Teams />
          <Route path="/calendar">
            <Calend />
          </Route>
      </Router>
    </div>
  );
}

export default App;
