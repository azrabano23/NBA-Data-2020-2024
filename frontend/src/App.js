import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [teamName, setTeamName] = useState("");
  const [playerName, setPlayerName] = useState("");
  const [recentGames, setRecentGames] = useState([]);
  const [playerStats, setPlayerStats] = useState([]);

  const fetchRecentGames = async () => {
    try {
      const response = await axios.get("/api/recent_games", {
        params: { team_name: teamName, num_games: 5 },
      });
      setRecentGames(response.data);
    } catch (error) {
      console.error("Error fetching recent games:", error);
    }
  };

  const fetchPlayerStats = async () => {
    try {
      const response = await axios.get("/api/player_stats", {
        params: { player_name: playerName },
      });
      setPlayerStats(response.data);
    } catch (error) {
      console.error("Error fetching player stats:", error);
    }
  };

  return (
    <div className="App">
      <h1>NBA Fan AI Program</h1>
      <div className="section">
        <h2>Get Recent Games</h2>
        <input
          type="text"
          placeholder="Enter team name"
          value={teamName}
          onChange={(e) => setTeamName(e.target.value)}
        />
        <button onClick={fetchRecentGames}>Fetch Games</button>
        <ul>
          {recentGames.map((game, index) => (
            <li key={index}>
              {game.GAME_DATE} - {game.MATCHUP} - {game.WL} - {game.PTS} points
            </li>
          ))}
        </ul>
      </div>
      <div className="section">
        <h2>Get Player Stats</h2>
        <input
          type="text"
          placeholder="Enter player name"
          value={playerName}
          onChange={(e) => setPlayerName(e.target.value)}
        />
        <button onClick={fetchPlayerStats}>Fetch Stats</button>
        <ul>
          {playerStats.map((stat, index) => (
            <li key={index}>
              {stat.game_date}: {stat.points} points, {stat.assists} assists,{" "}
              {stat.reboundsTotal} rebounds
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
