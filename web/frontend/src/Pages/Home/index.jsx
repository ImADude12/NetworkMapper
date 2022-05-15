import React, { useEffect, useState } from "react";
import { Graph } from "./Graph";
import axios from "axios";
import { Navbar } from "../../Shared/Navbar";
import { Button } from "../../Shared/Button";
import styled, { useTheme } from "styled-components";
import PuffLoader from "react-spinners/PuffLoader";
import search from "../../assets/icons/search.svg";
import { Image } from "../../Shared/Image";

const GraphWrapper = styled.div`
  height: 800px;
  width: 90%;
  flex-direction: column;
  display: flex;
  justify-content: center;
  align-items: center;
`;
const Container = styled.div`
  height: calc(100% - 80px);
  flex-direction: column;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
`;

export const Home = () => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const theme = useTheme();

  const onScan = () => {
    setIsLoading(true);
    axios.get("http://localhost:3030/").then((res) => {
      setData(res.data);
      setIsLoading(false);
    });
  };

  return (
    <>
      <Navbar />
      <Container>
        <GraphWrapper>
          {isLoading ? (
            <PuffLoader color={theme.colors.primary} />
          ) : (
            <Graph data={data} />
          )}
        </GraphWrapper>
        <Button size="lg" onClick={() => onScan()}>
          Scan
          <Image style={{ marginInlineStart: theme.spacing(1) }} src={search} />
        </Button>
      </Container>
    </>
  );
};
