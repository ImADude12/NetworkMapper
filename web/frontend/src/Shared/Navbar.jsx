import styled from "styled-components";
import { Image } from "./Image";
import Logo from "../assets/images/Logo.svg";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useState } from "react";

const Wrapper = styled.div`
  display: flex;
  border-bottom: gray;
  box-shadow: 0 2px 32px 0 rgb(0 0 0 / 20%);
  & > a,
  div {
    ${({ isRight }) =>
      isRight
        ? "border-left: 1px solid white;"
        : "border-right: 1px solid white;"}
  }
`;

const Container = styled.nav`
  display: none;
  @media ${({ theme }) => theme.media.fromMobile} {
    display: flex;
  }
  background-color: ${({ theme }) => theme.colors.primary};
  justify-content: space-between;
  height: 80px;
`;

const NavItem = styled.a`
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const LogoContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  :hover {
    cursor: pointer;
  }
  height: 100%;
`;

const MobileContainer = styled.div`
  display: flex;
  @media ${({ theme }) => theme.media.fromMobile} {
    display: none;
  }
  background-color: ${({ theme }) => theme.colors.primary};
  align-items: center;
  justify-content: space-between;
  img {
    max-width: 200px;
  }
`;

const Hamburger = styled.div`
  width: 40px;
  height: 45px;
  margin: 12px;
  position: relative;
  transform: rotate(0deg);
  transition: 0.5s ease-in-out;
  cursor: pointer;

  span {
    display: block;
    position: absolute;
    height: 8px;
    width: 100%;
    background: white;
    border-radius: 9px;
    opacity: 1;
    left: 0;
    transform: rotate(0deg);
    transition: 0.25s ease-in-out;
  }

  span:nth-child(1) {
    top: 0px;
  }

  span:nth-child(2),
  span:nth-child(3) {
    top: 18px;
  }

  span:nth-child(4) {
    top: 36px;
  }

  &.open span:nth-child(1) {
    top: 18px;
    width: 0%;
    left: 50%;
  }

  &.open span:nth-child(2) {
    transform: rotate(45deg);
  }

  &.open span:nth-child(3) {
    transform: rotate(-45deg);
  }

  &.open span:nth-child(4) {
    top: 18px;
    width: 0%;
    left: 50%;
  }
`;

const MobileMenu = styled.div`
  overflow: hidden;
  max-height: ${({ open }) => (open ? "500px" : "0")};
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: 500ms ease-in-out;
`;

const MobileMenuItem = styled.div`
  width: 100%;
  font-weight: 700;
  text-align: center;
  padding: 12px 0;
  color: ${({ theme }) => theme.colors.primary};
  border-bottom: 2px solid ${({ theme }) => theme.colors.primary};
  &:hover {
    cursor: pointer;
  }
`;

export const Navbar = () => {
  const navigate = useNavigate();

  const logout = () => {
    axios.post("http://localhost:3030/logout").then(() => navigate("/"));
  };

  const [open, setOpen] = useState(false);

  return (
    <>
      <Container>
        <Wrapper>
          <LogoContainer>
            <Image src={Logo} />
          </LogoContainer>
          <NavItem onClick={() => navigate("/home")}>Home</NavItem>
          <NavItem onClick={() => navigate("/config")}>Configuration</NavItem>
        </Wrapper>
        <Wrapper isRight>
          <NavItem onClick={() => logout()} style={{ padding: "0 56px" }}>
            Logout
          </NavItem>
        </Wrapper>
      </Container>
      <div>
        <MobileContainer>
          <Image src={Logo} />
          <Hamburger className={open && "open"} onClick={() => setOpen(!open)}>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </Hamburger>
        </MobileContainer>
        <MobileMenu open={open}>
          <MobileMenuItem onClick={() => navigate("/home")}>
            Home
          </MobileMenuItem>
          <MobileMenuItem onClick={() => navigate("/config")}>
            Configuration
          </MobileMenuItem>
          <MobileMenuItem onClick={() => logout()}>Logout</MobileMenuItem>
        </MobileMenu>
      </div>
    </>
  );
};
