import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import PixelbotSummaryPage from './pages/PixelbotSummaryPage'
import PixelbotChildRecapPage from './pages/PixelbotChildRecapPage'
import PixelbotSessionDetailPage from './pages/PixelbotSessionDetailPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/pixelbot" element={<Navigate to="/pixelbot/summary" replace />} />
        <Route path="/pixelbot/summary" element={<PixelbotSummaryPage />} />
        <Route path="/pixelbot/child/:childId" element={<PixelbotChildRecapPage />} />
        <Route path="/pixelbot/child/:childId/session/:sessionId" element={<PixelbotSessionDetailPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
