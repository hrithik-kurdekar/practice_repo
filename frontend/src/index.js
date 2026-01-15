import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // Import the CSS file
import App from './App'; // Import your main App component

// Create the root container for the application
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component inside the root container
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);