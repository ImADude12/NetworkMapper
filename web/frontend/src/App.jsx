import React, { useEffect, useState } from "react";
import { Graph } from "./Graph";
import axios from "axios";

const App = () => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const onScan = () => {
    setIsLoading(true);
    axios.get("http://localhost:3030/").then((res) => {
      setData(res.data);
      setIsLoading(false);
    });
  };

  return (
    <div className="container">
      {isLoading ? (
        <div style={{ height: "500px",display:'flex',alignItems:'center',justifyContent:'center' }}>
          <p> Loading...</p>
        </div>
      ) : (
        <Graph data={data} />
      )}
      <button onClick={() => onScan()}>Scan</button>
    </div>
  );
};

export default App;
