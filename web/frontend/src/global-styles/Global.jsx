import { createGlobalStyle } from "styled-components";
import Roboto from "../assets/fonts/Roboto/Roboto-Regular.ttf";
import RobotoThin from "../assets/fonts/Roboto/Roboto-Thin.ttf";
export const GlobalStyles = createGlobalStyle`
 @font-face {
    font-family: 'Roboto';
    src: url(${Roboto});
  }

 @font-face {
    font-family: 'Roboto';
    src: url(${RobotoThin});
  }

* {
box-sizing: border-box;
  margin: 0;
}

h1{
  font-size: ${({ theme }) => theme.fontSize.medium};
    @media ${({ theme }) => theme.media.fromMobile}{
      font-size: ${({ theme }) => theme.fontSize.large};
    }
}

h2{
  font-size: ${({ theme }) => theme.fontSize.medium}
}
p{
  font-size: ${({ theme }) => theme.fontSize.small}
}

#root,body,html{
  height: 100%;
  width: 100%;
  background-color: ${({ theme }) => theme.colors.background};
  font-family: 'Roboto';
}
`;
