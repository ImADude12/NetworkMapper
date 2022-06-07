import styled from "styled-components";
import { Image } from "./Image";
import Logo from "../assets/images/Logo.svg";
import { useNavigate } from "react-router-dom";
import axios from "axios";

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
  display: flex;
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

export const Navbar = () => {
  const navigate = useNavigate();

  const logout = () => {
    axios.post("http://localhost:3030/logout").then(() => navigate("/"));
  };
  return (
    <Container>
      <Wrapper>
        <LogoContainer>
          <Image src={Logo} />
        </LogoContainer>
        <NavItem onClick={() => navigate("/home")}>Home</NavItem>
        <NavItem>Configuration</NavItem>
      </Wrapper>
      <Wrapper isRight>
        <NavItem onClick={() => logout()} style={{ padding: "0 56px" }}>
          Logout
        </NavItem>
      </Wrapper>
    </Container>
  );
};
