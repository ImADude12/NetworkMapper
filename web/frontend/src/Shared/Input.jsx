import styled from "styled-components";

export const Input = styled.input`
  outline: 0;
  width: 100%;
  border-radius: 20px;
  background-color: ${({ theme }) => theme.colors.secondary};
  border: 1px solid ${({ theme }) => theme.colors.primary};
  padding: 12px 16px;
  font-size: ${({ theme }) => theme.fontSize.small};
  ::placeholder {
    font-weight: 600;
  }
  :focus {
    background-color: white;
  }
  transition: all 300ms ease-in-out;
`;
