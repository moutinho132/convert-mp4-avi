import { ThemeProvider, createTheme, CssBaseline } from '@mui/material'
import './App.css'

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="App">
        <h1>MP4 to AVI Converter</h1>
        <p>Sistema de conversión de archivos de video</p>
      </div>
    </ThemeProvider>
  )
}

export default App
