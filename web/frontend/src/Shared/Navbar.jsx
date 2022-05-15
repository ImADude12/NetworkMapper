import styled from "styled-components";
import { Button } from "./Button";
import { Image } from "./Image";
import Logo from "../assets/images/Logo.svg";

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

const Navitem = styled.a`
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

export const Navbar = () => (
  <Container>
    <Wrapper>
      <LogoContainer>
        <Image src={Logo} />
      </LogoContainer>
      <Navitem>Home</Navitem>
      <Navitem>Configuration</Navitem>
    </Wrapper>
    <Wrapper isRight>
      <Navitem style={{ padding: "0 56px" }}>Logout</Navitem>
    </Wrapper>
  </Container>
);
