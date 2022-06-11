import styled from "styled-components";
import { Button } from "../../Shared/Button";
import { Input } from "../../Shared/Input";
import networkPerson from "../../assets/images/network-person.png";
import { Image } from "../../Shared/Image";
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Container = styled.form`
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

export const Form = () => {
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });
  let navigate  = useNavigate();

  const onChangeHandler = (ev) => {
    const { name, value } = ev.target;
    setCredentials((prev) => ({ ...prev, [name]: value }));
  };

  const onSubmitCred = (ev) => {
    ev.preventDefault();
    axios
      .post("http://localhost:3030/auth", { credentials })
      .then((res) => {
        if (res.status === 200) {
          navigate("/home");
        }
      })
      .catch((err) => console.log(err));
  };

  return (
    <Container onSubmit={onSubmitCred}>
      <Image src={networkPerson}></Image>
      <Input
        value={credentials.username}
        name="username"
        onChange={onChangeHandler}
        placeholder="Username"
      />
      <Input
        value={credentials.password}
        autoComplete="true"
        name="password"
        onChange={onChangeHandler}
        placeholder="Password"
        type="password"
      />
      <Button type="submit" size="sm">
        Login
      </Button>
    </Container>
  );
};
