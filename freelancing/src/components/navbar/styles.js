import styled, { css } from "styled-components";
import { NavLink } from "react-router-dom";

export const Nav = styled.div`
    background-color: ${props => props.theme.main}
    padding: 10px 20px;

`;

export const NavHeader = styled.div`
  display: flex;
  align-items: center;
  margin: 0 auto;
  width: 100%;
`;

export const NavLeft = styled.div`
  width: 70%;
`;

export const NavRight = styled.div`
  width: 30%;
  display: flex;
  justify-content: flex-end;
`;

export const MenuLink = styled(NavLink)`
  margin-left: 10px;
  margin-right: 10px;
  padding: 8px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  &:hover {
    color: ${props => props.theme.bg};
  }

  ${props =>
    props.button &&
    css`
      border: 2px solid ${props => props.theme.bg};
      border-radius: 5px;
      font-weight: 600;
      width: 50px;
      &:hover {
        color: ${props => props.theme.accent};
        background-color: ${props => props.theme.bg};
      }
    `}
`;

export const Logo = styled.a`
  font-size: 28px;
  font-family: "Comic Sans MS";
  font-weight: 600;
`;
