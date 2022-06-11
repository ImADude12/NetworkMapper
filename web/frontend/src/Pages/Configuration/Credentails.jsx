import { useState } from "react";
import styled from "styled-components";
import { Button } from "../../Shared/Button";
import { Input } from "../../Shared/Input";
import trash from "../../assets/icons/trash.svg";
import { useLocalStorage } from "../../Hooks/useLocalStorage";
const Header = styled.h1`
  text-align: center;
  color: ${({ theme }) => theme.colors.primary};
  margin-bottom: 56px;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  button {
    align-self: flex-end;
    max-width: 220px;
  }
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  margin-top: 32px;
  @media ${({ theme }) => theme.media.fromMobile} {
    margin-top: 112px;
  }
`;

const Wrapper = styled.div`
  display: flex;
  margin-bottom: 12px;
  input:first-child {
    margin-inline-end: 24px;
  }
`;

const UsersTable = styled.div`
  margin-top: 24px;
  border: 2px solid black;
  overflow: auto;
  height: 500px;
`;

const UserList = styled.ul`
  display: flex;
  flex-direction: column;
  padding: 0;
`;

const UserItem = styled.li`
  align-items: center;
  justify-content: space-between;
  padding: 8px;
  list-style-type: none;
  display: flex;
  border-bottom: 2px solid black;

  p:not(:last-child) {
    margin-inline-end: 24px;
  }
`;

const Delete = styled.img`
  &:hover {
    cursor: pointer;
  }
`;
const InfoContainer = styled.div`
  align-items: center;
  display: flex;
  font-weight: 600;
`;

export const Credentials = () => {
  const [userList, setUserList] = useLocalStorage("userList", []);
  const [currCred, setCurrCred] = useState({
    username: "",
    password: "",
  });

  const onChangeHandler = (ev) => {
    const { name, value } = ev.target;
    setCurrCred((prev) => ({ ...prev, [name]: value }));
  };

  const onSubmitCred = (ev) => {
    ev.preventDefault();
    const newUserList = [...userList, currCred];
    setUserList(newUserList);
  };

  const onDeleteCred = (key) => {
    const newUserList = userList.filter((user, idx) => idx !== key);
    setUserList(newUserList);
  };

  return (
    <Container>
      <Header>Users Credentials</Header>
      <Form onSubmit={onSubmitCred}>
        <Wrapper>
          <Input
            name="username"
            placeholder="Username"
            onChange={onChangeHandler}
          />
          <Input
            name="password"
            placeholder="Password"
            onChange={onChangeHandler}
          />
        </Wrapper>
        <Button type="submit">Add +</Button>
      </Form>

      <UsersTable>
        <UserList>
          {userList ? (
            userList.map((user, key) => {
              return (
                <UserItem key={key}>
                  <InfoContainer>
                    <p>{user.username}</p>
                    <p>:</p>
                    <p>{user.password}</p>
                  </InfoContainer>
                  <Delete src={trash} onClick={() => onDeleteCred(key)} />
                </UserItem>
              );
            })
          ) : (
            <h1>No Users Yet..</h1>
          )}
        </UserList>
      </UsersTable>
    </Container>
  );
};
