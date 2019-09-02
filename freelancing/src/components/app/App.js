import React from 'react'
import { ThemeProvider } from 'styled-components'
import theme, { invertTheme } from './theme';
import Navbar from '../navbar/Navbar';

const App = () => {
  return (
    <ThemeProvider theme={invertTheme}>
      <Navbar />
    </ThemeProvider>
  )
}

export default App
