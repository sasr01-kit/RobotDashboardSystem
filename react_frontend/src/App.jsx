import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Homepage from './pages/homepage/Homepage.jsx';
import Pixelbot from './pages/pixelbot/Pixelbot.jsx';
import Turtlebot from './pages/turtlebot/Turtlebot.jsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/homepage" replace />} />
        <Route path="/homepage/*" element={<Homepage />} />
        <Route path="/pixelbot/*" element={<Pixelbot />} />
        <Route path="/turtlebot/*" element={<Turtlebot />} />
        {/*Here you can add in more routes for more robots after adding their resources
        in the file tree*/}
        <Route path="*" element={<Navigate to="./homepage" replace />} /> {"Fallback"}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
