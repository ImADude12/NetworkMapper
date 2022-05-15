import styled from "styled-components";
import { Button } from "../../Shared/Button";
import { Input } from "../../Shared/Input";
import networkPerson from "../../assets/images/network-person.png";
import { Image } from "../../Shared/Image";

const Container = styled.div`
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 90%;
  max-width: 700px;
  & > *:not(:last-child) {
    margin-block-end: ${({ theme }) => theme.spacing(2)};
  }
  button {
    width: 50%;
  }
`;

export const Form = () => (
  <Container>
    <Image src={networkPerson}></Image>
    <Input placeholder="Email" />
    <Input placeholder="Password" type="password" />
    <Button type="submit" size="sm">
      Login
    </Button>
  </Container>
);
