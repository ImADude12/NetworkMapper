import React, { useEffect, useState } from "react";
import { Graph } from "./Graph";
import axios from "axios";
const App = () => {
  // const data = {
  //   name: "🙂",
  //   children: [
  //     {
  //       name: "🙂",
  //       children: [
  //         {
  //           name: "😀",
  //         },
  //         {
  //           name: "😁",
  //         },
  //         {
  //           name: "🤣",
  //         },
  //       ],
  //     },
  //     {
  //       name: "😔",
  //     },
  //   ],
  // };
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:3030/").then((res) => {
      const { nodes, links } = res.data;
      setData(res.data);
    });
  }, []);

  return <Graph data={data} />;
};

export default App;
