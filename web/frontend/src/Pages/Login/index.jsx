import styled from "styled-components";
import { Form } from "./Form";

const Container = styled.div`
  text-align: center;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const Headline = styled.h1`
  margin-block-end: ${({ theme }) => theme.spacing(10)};
  @media ${({ theme }) => theme.media.fromTablet} {
    margin-block-end: ${({ theme }) => theme.spacing(20)};
    font-weight: bold;
  }
`;

const Login = () => (
  <Container>
    <Headline>Login to Your Account</Headline>
    <Form />
  </Container>
);

export default Login;
