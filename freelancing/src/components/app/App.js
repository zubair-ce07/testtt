import React from 'react'
import { ThemeProvider } from 'styled-components'
import theme from './theme';
import Navbar from '../navbar/Navbar';

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <Navbar />
    </ThemeProvider>
  )
}

export default App
