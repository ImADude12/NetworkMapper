import React, { useRef, useEffect, useState } from "react";
import {
  select,
  forceSimulation,
  forceManyBody,
  forceLink,
  forceCollide,
  map,
} from "d3";
// import useResizeObserver from "./useResizeObserver";

/**
 * Component, that renders a force layout for hierarchical data.
 */

export const Graph = ({ data }) => {
  const [size, setSize] = useState({ height: 500, width: 500 });
  const [loading, setLoading] = useState(false);
  const svgRef = useRef();

  // will be called initially and on every data change
  useEffect(() => {
    if (!size || !data) return;

    const svg = select(svgRef.current);

    // centering workaround
    svg.attr("viewBox", [
      -size.width / 2,
      -size.height / 2,
      size.width,
      size.height,
    ]);

    const { nodes, links } = data;

    forceSimulation(nodes)
      .force(
        "link",
        forceLink(links).id(({ id }) => id)
      )
      .force("charge", forceManyBody().strength(-30))
      .force("collide", forceCollide(30))
      .on("tick", () => {
        // links
        svg
          .selectAll(".link")
          .data(links)
          .join("line")
          .attr("class", "link")
          .attr("stroke", "black")
          .attr("fill", "none")
          .attr("x1", (link) => link.source.x)
          .attr("y1", (link) => link.source.y)
          .attr("x2", (link) => link.target.x)
          .attr("y2", (link) => link.target.y);

        // nodes
        svg
          .selectAll(".node")
          .data(nodes)
          .join("circle")
          .attr("class", "node")
          .attr("r", 10)
          .attr("cx", (node) => node.x)
          .attr("cy", (node) => node.y);

        svg
          .selectAll(".label")
          .data(nodes)
          .join("text")
          .attr("class", "label")
          .attr("text-anchor", "middle")
          .attr("font-size", 10)
          .text((node) => `${node.type} \n ${node.ip} \n ${node.os}`)
          .attr("x", (node) => node.x)
          .attr("y", (node) => node.y + 50);
      });
  }, [data]);

  return (
    <div style={{ height: size.height + "px", width: size.width + "px" }}>
      <svg ref={svgRef}></svg>
    </div>
  );
};
