import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import WebSocketProvider from './modules/turtlebot/WebsocketUtil/WebsocketProvider.jsx'

createRoot(document.getElementById('root')).render(

    <WebSocketProvider>
      <App />
    </WebSocketProvider>

)
