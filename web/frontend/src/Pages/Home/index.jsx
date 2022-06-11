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
import finger from "../../assets/images/finger.png";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "../../Hooks/useLocalStorage";
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

const FingerContainer = styled.div`
  display: flex;
  position: relative;
  width: 100%;
  height: 100%;
`;

const FingerImg = styled.img`
  transform: rotate(90deg);
  animation: MoveUpDown 1s linear infinite;
  position: absolute;
  right: 10%;

  @media ${({ theme }) => theme.media.fromMobile} {
    right: 45%;
  }
  @keyframes MoveUpDown {
    0%,
    100% {
      transform: translateY(100px);
    }
    50% {
      transform: translateY(0);
    }
  }
`;

export const Home = () => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isStarted, setIsStarted] = useState(false);
  const [users] = useLocalStorage("userList");
  const theme = useTheme();

  const navigate = useNavigate();

  const onScan = () => {
    console.log(users);
    setIsStarted(true);
    setIsLoading(true);
    axios
      .post("http://localhost:3030/scan", { users })
      .then((res) => {
        setData(res.data);
        setIsLoading(false);
      })
      .catch(() => navigate("/"));
  };

  const [isOpen, setIsOpen] = useState(false);
  const [modalChildren, setModalChildren] = useState();

  const onOpenModal = useCallback((props) => {
    setIsOpen(true);
    console.log(props);
    setModalChildren(
      <>
        <img style={{ height: "200px", width: "80%" }} alt="" src={props.img} />
        <div style={{ textAlign: "center" }}>
          <p>{props.ip}</p>
          <p>{props.os}</p>
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
      <Navbar currPage={"home"} />
      <Container>
        <GraphWrapper>
          {isStarted ? (
            isLoading ? (
              <PuffLoader color={theme.colors.primary} />
            ) : (
              <Graph data={data} onOpenModal={onOpenModal} />
            )
          ) : (
            <FingerContainer>
              <FingerImg src={finger} />
            </FingerContainer>
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
