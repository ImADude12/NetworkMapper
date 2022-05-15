import React, { useRef, useEffect, useState } from "react";
import * as d3 from "d3";
import computer from "../../assets/images/computer.svg";
import router from "../../assets/images/router.svg";

export const Graph = ({ data }) => {
  const [size] = useState({ height: 500, width: 500 });
  const svgRef = useRef();

  useEffect(() => {
    if (!size || !data) return;

    const svg = d3.select(svgRef.current);
    const { nodes, links } = data;

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3.forceLink(links).id((d) => d.id)
      )
      .force("charge", d3.forceManyBody().strength(-20))
      .force("collide", d3.forceCollide(30))
      .force("center", d3.forceCenter(size.width / 2, size.height / 2));

    svg.attr("viewBox", [0, 0, size.width, size.height]);

    const link = svg
      .append("g")
      .attr("stroke", "black")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", 3);

    const nodeContainer = svg
      .append("g")
      .selectAll(".node")
      .data(nodes, (d) => d.id)
      .attr("class", "node")
      .join("g");

    const circle = nodeContainer
      .append("circle")
      .attr("r", 20)
      .attr("fill", "#ebf4ff");

    const image = nodeContainer
      .append("svg:image")
      .attr("width", 20)
      .attr("height", 24)
      .attr("xlink:href", (node) =>
        node.type === "Computer" ? computer : router
      );

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);
      image.attr("x", (d) => d.x - 10).attr("y", (d) => d.y - 10);
      circle.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
    });
  }, [data]);

  return <svg style={{ height: "100%", width: "100%" }} ref={svgRef}></svg>;
};
