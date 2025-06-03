import React, { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

function App() {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchTrends() {
      try {
        const response = await axios.get("/api/trends");
        setTrends(response.data);
      } catch (error) {
        console.error("Error fetching trends:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchTrends();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Trend2Product Dashboard</h1>
      <h2>Latest Trends</h2>
      <ul>
        {trends.map((trend) => (
          <li key={trend.id}>
            <strong>{trend.title}</strong>: {trend.summary}
          </li>
        ))}
      </ul>

      <h2>Trend Popularity Over Time</h2>
      <LineChart width={600} height={300} data={trends}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
        <Line type="monotone" dataKey="popularity_score" stroke="#8884d8" />
      </LineChart>
    </div>
  );
}

export default App;
