import React, { useState, useEffect } from 'react';
import './index.css';

// Get the API URL from the environment variable (set by docker-compose)
// Default to 8000 for local development outside of Docker
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

function App() {
    const [votes, setVotes] = useState({});
    const [message, setMessage] = useState('Loading poll data...');

    // 1. Function to fetch the current vote counts
    const fetchVotes = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/votes`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setVotes(data);
            setMessage('Poll results updated!');
        } catch (error) {
            console.error("Could not fetch votes:", error);
            setMessage("Error fetching votes. Check backend connection.");
        }
    };

    // 2. Handle casting a vote
    const handleVote = async (color) => {
        setMessage(`Casting vote for ${color}...`);
        try {
            const response = await fetch(`${API_BASE_URL}/vote/${color}`, {
                method: 'POST',
            });
            if (!response.ok) {
                // This will catch the 404 from FastAPI if the color doesn't exist
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setMessage(data.message);

            // Optimistically update the local state with the new count
            setVotes(prevVotes => ({
                ...prevVotes,
                [color]: data.new_count
            }));

        } catch (error) {
            console.error("Could not cast vote:", error);
            setMessage("Error casting vote. Please try again.");
        }
    };

    // Effect to load data on mount and refresh periodically
    useEffect(() => {
        fetchVotes();
        // Refresh votes every 3 seconds for a dynamic feel
        const interval = setInterval(fetchVotes, 3000);
        return () => clearInterval(interval); // Cleanup function
    }, []);

    return (
        <div className="container">
            <h1>🗳️ Favorite Color Poll</h1>

            <p className="message">{message}</p>

            <div className="results-grid">
                {Object.entries(votes).map(([color, count]) => (
                    <div key={color} className="poll-item">
                        <div className="poll-header">
                            <span className="color-name" style={{ color: color }}>{color}</span>
                            <span className="vote-count">Votes: **{count}**</span>
                        </div>
                        <button
                            className="vote-button"
                            onClick={() => handleVote(color)}
                            style={{ backgroundColor: color, color: color === 'Yellow' ? 'black' : 'white' }}
                        >
                            Vote for {color}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;