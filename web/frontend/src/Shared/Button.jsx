import styled from "styled-components";

export const Button = styled.button`
  ${({ size }) => {
    switch (size) {
      case "sm":
        return `padding: 10px 10px; font-size: 1rem;`;
      case "lg":
        return `padding: 15px 30px; font-size: 2rem;`;
      case "md":
      default:
        return `padding: 10px; 20px; font-size: 1.5rem;`;
    }
  }}
  background: ${({ variant, theme }) =>
    variant === "secondary" ? theme.colors.secondary : theme.colors.primary};
  color: ${({ variant, theme }) =>
    variant === "secondary"
      ? theme.colors.secondaryText
      : theme.colors.primaryText};
  display: flex;
  align-items: center;
  justify-content: ${({ justify }) =>
    justify === "around"
      ? "space-around"
      : justify === "between"
      ? "space-between"
      : "center"};
  letter-spacing: 0.25px;
  border-radius: 20px;
  border: none;
  &:hover,
  &:active {
    background: ${({ theme, variant }) =>
      variant === "secondary"
        ? theme.colors.secondaryHover
        : theme.colors.primaryHover};
  }
  cursor: pointer;
  ${({ disabled }) =>
    disabled &&
    `
  cursor: not-allowed;
  pointer-events: none;
  opacity: 0.4;
  `}
`;
