import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Homepage from './modules/robotSelection/Homepage.jsx';
import Pixelbot from './modules/pixelbot/Pixelbot.jsx';
import Turtlebot from './modules/turtlebot/Turtlebot.jsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/homepage" replace />} />
        <Route path="/homepage/*" element={<Homepage />} />
        <Route path="/pixelbot/*" element={<Pixelbot />} />
        <Route path="/turtlebot/*" element={<Turtlebot />} />
        {/* Add more routes for more robots after adding their resources in the tree */}
        <Route path="*" element={<Navigate to="/homepage" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
