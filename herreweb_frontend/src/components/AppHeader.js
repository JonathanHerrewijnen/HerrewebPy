/* eslint-disable jsx-a11y/accessible-emoji */
import React, { useState, useEffect } from "react";
import "../static/AppHeader.css";
import { CSSTransition } from "react-transition-group";
import logo from '../static/logo.svg';

export default function AppHeader() {
  const [isNavVisible, setNavVisibility] = useState(false);
  const [isSmallScreen, setIsSmallScreen] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(max-width: 700px)");
    mediaQuery.addListener(handleMediaQueryChange);
    handleMediaQueryChange(mediaQuery);

    return () => {
      mediaQuery.removeListener(handleMediaQueryChange);
    };
  }, []);

  const handleMediaQueryChange = mediaQuery => {
    if (mediaQuery.matches) {
      setIsSmallScreen(true);
    } else {
      setIsSmallScreen(false);
    }
  };

  const toggleNav = () => {
    setNavVisibility(!isNavVisible);
  };

  return (
    <header className="Header">
      <img src={logo} className="Logo" alt="logo" />
      <CSSTransition
        in={!isSmallScreen || isNavVisible}
        timeout={350}
        classNames="NavAnimation"
        unmountOnExit
      >
        <nav className="Nav">
          <a href="/">Projects</a>
          <a href="/">Blogs</a>
          <a href="/">About Us</a>
        </nav>
      </CSSTransition>
      <button onClick={toggleNav} className="Burger">
        🍔
      </button>
    </header>
  );
}
