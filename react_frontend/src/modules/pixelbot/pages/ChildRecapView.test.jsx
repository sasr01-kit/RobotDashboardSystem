import React from 'react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ChildRecapView from './ChildRecapView'
import { usePixelbotRecap } from '../hooks/usePixelbotRecap'

vi.mock('../hooks/usePixelbotRecap')
vi.mock('../components/BarChart', () => ({ default: () => React.createElement('div', { 'data-testid': 'bar-chart' }) }))
vi.mock('../components/LineChart', () => ({ default: () => React.createElement('div', { 'data-testid': 'line-chart' }) }))

const mockChild = {
  name: 'Child One',
  drawings: [],
  metricValues: {
    totalSessions: 2,
    sessionTrendPercentage: '10.0',
    totalWordCount: 100,
    averageWordCount: 50,
    averageIntimacyScore: 0.5,
    averageStrokeCount: 8,
    averageNumberColors: 3,
    averageFilledArea: 25,
    averageNumberObjects: 2,
    mostCommonObjects: ['ball'],
    objectDiversity: 0.5,
  },
  sessionFrequencyData: [],
  wordCountData: [],
  speechTimeData: [],
  intimacyScoreData: [],
}

function renderWithRouter(childId = 'c1') {
  return render(
    <MemoryRouter initialEntries={[`/pixelbot/session/${childId}`]}>
      <Routes>
        <Route path="/pixelbot/session/:childId" element={<ChildRecapView />} />
      </Routes>
    </MemoryRouter>
  )
}

describe('ChildRecapView', () => {
  beforeEach(() => {
    usePixelbotRecap.mockReturnValue({ child: mockChild, isLoading: false })
  })

  it('T27: shows child name, Recap title and trend metrics', () => {
    renderWithRouter()
    expect(screen.getByText(/Child One - Recap/)).toBeInTheDocument()
    expect(screen.getByText('Total Sessions')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(screen.getByText('Drawing(s)')).toBeInTheDocument()
    expect(screen.getByText('Average Stroke Count:')).toBeInTheDocument()
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument()
    expect(screen.getAllByTestId('line-chart').length).toBeGreaterThan(0)
  })

  it('shows Loading when child is loading', () => {
    usePixelbotRecap.mockReturnValue({ child: null, isLoading: true })
    renderWithRouter()
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })
})
