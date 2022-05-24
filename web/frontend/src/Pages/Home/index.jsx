import React, { useCallback, useState } from "react";
import { Graph } from "./Graph";
import axios from "axios";
import { Navbar } from "../../Shared/Navbar";
import { Button } from "../../Shared/Button";
import styled, { useTheme } from "styled-components";
import PuffLoader from "react-spinners/PuffLoader";
import search from "../../assets/icons/search.svg";
import { Image } from "../../Shared/Image";
import Modal from "./Modal";

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

  const [isOpen, setIsOpen] = useState(false);
  const [modalChildren, setModalChildren] = useState();

  const onOpenModal = useCallback((props) => {
    setIsOpen(true);
    console.log(props);
    setModalChildren(
      <>
        <img style={{ height: "200px", width: "80%" }} alt="" src={props.img} />
        <div>
          <p>IP: {props.ip}</p>
          <p>OS: {props.os}</p>
        </div>
      </>
    );
  }, []);

  return (
    <>
      <Modal
        isOpen={isOpen}
        children={modalChildren}
        handleClose={() => setIsOpen(false)}
      />
      <Navbar />
      <Container>
        <GraphWrapper>
          {isLoading ? (
            <PuffLoader color={theme.colors.primary} />
          ) : (
            <Graph data={data} onOpenModal={onOpenModal} />
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
