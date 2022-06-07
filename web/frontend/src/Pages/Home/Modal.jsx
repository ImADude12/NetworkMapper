import styled from "styled-components";

const ModalContainer = styled.div`
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  position: absolute;
  height: 100%;
  width: 100%;
  z-index: 4;
  background-color: #83828247;
`;

const ModalContent = styled.div`
  position: absolute;
  z-index: 5;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
  position: relative;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  width: 50%;
  height: 80%;
  padding: 40px;
  p {
    font-size: 2rem;
    font-weight: 600;
    margin: 12px;
  }
`;

const CloseButton = styled.button`
  border: none;
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: transparent;
  &:hover {
    cursor: pointer;
  }
`;

export const Modal = ({ children, isOpen, handleClose }) => {
  return (
    isOpen && (
      <ModalContainer onClick={handleClose}>
        <ModalContent onClick={(ev) => ev.stopPropagation()}>
          {children}
          <CloseButton onClick={handleClose}>X</CloseButton>
        </ModalContent>
      </ModalContainer>
    )
  );
};
export default Modal;
