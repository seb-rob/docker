import React, { useState } from 'react';
import './App.css';

function App() {
  // State to hold the counter value
  const [count, setCount] = useState(0);

  // Function to handle increment
  const increment = () => {
    setCount(count + 1);
  };

  // Function to handle decrement
  const decrement = () => {
    setCount(count - 1);
  };

  // Function to reset the counter
  const reset = () => {
    setCount(0);
  };

  return (
    <div className="App">
      <h1>React Counter App</h1>
      <div className="counter">
        <button onClick={decrement} className="button">-</button>
        <span className="count">{count}</span>
        <button onClick={increment} className="button">+</button>
      </div>
      <button onClick={reset} className="reset-button">Reset</button>
    </div>
  );
}

export default App;
