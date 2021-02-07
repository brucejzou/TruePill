import React, { Component } from 'react';
import './App.css';
import logo from "./logo-small.png";
import {getCurrentTab} from "./common/Utils";
import TrafficContainer from "./components/TrafficContainer";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            traffic: {}
        };
    }

    componentDidMount() {
        getCurrentTab((tab) => {
            chrome.runtime.sendMessage({type: 'popupInit', tabId: tab.id}, (response) => {
                if (response) {
                    this.setState({
                        traffic: Object.assign(this.state.traffic, response)
                        
                    });
                }
            });
        });
    }

    render() {
      return (
          <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <p>
              True Pill coming soon.
            </p>
    
          </header>
        </div>
      );
    }

    // render() {
    //     return (
    //       <div className="App">
    //         <header className="App-header">
    //           <h1 className="App-title">True Pill</h1>
    //           <img src={logo} className="App-logo" alt="logo" />
    //         </header>
    //         <p className="App-intro">
    //             Coming Soon.
    //         </p>
    //       </div>
    //     );
    // }
}

export default App;
// 
// import './App.css';

// function App() {
//   return (
  //   <div className="App">
  //     <header className="App-header">
        
  //       <p>
  //         True Pill coming soon.
  //       </p>

  //     </header>
  //   </div>
  // );
// }

// export default App;

