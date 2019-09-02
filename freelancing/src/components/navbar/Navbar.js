import React from 'react'
import { Nav, NavHeader, NavRight, NavLeft, MenuLink, Logo } from './styles';

const Navbar = () => {
    return (
        <Nav>
            <NavHeader>
                <NavLeft>
                    <Logo>Fiverr</Logo>
                </NavLeft>
                <NavRight>
                    <MenuLink>
                        Sign In
                    </MenuLink>
                    <MenuLink button>
                        Join
                    </MenuLink>
                </NavRight>
            </NavHeader>
        </Nav>
    )
}

export default Navbar
