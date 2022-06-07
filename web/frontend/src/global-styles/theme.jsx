const size = {
  mobile: "767.98px",
  tablet: "1270.98px",
};

const fontSize = {
  small: "1rem",
  medium: "3rem",
  large: "5rem",
};

const media = {
  fromMobile: `(min-width: ${size.mobile})`,
  fromTablet: `(min-width: ${size.tablet})`,
};

export const theme = {
  fontSize,
  colors: {
    primary: `#3F72AF`,
    primaryText: "white",
    primaryHover: `#5d84b4`,
    secondary: `#DBE2EF`,
    secondaryText: "black",
    secondaryHover: `#F9F7F7`,
  },
  media,
  spacing: (number) => 8 * number + "px",
};
