import React from 'react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import PixelbotSummaryView from './PixelbotSummaryView'
import { usePixelbotSummary } from '../hooks/usePixelbotSummary'

vi.mock('../hooks/usePixelbotSummary')
vi.mock('../components/CalendarHeatMap', () => ({ default: ({ id }) => React.createElement('div', { id, 'data-testid': 'calendar-heatmap' }) }))

const mockSummaryStats = {
  totalSessions: 42,
  avgSessionsPerChild: 4,
  sessionsPerDay: 2,
  sessionsGrowthRate: 10,
  dailySessionCounts: [],
  colorScale: [],
}

describe('PixelbotSummaryView', () => {
  beforeEach(() => {
    usePixelbotSummary.mockReturnValue({
      summaryStats: mockSummaryStats,
      isLoading: false,
    })
  })

  it('T20/T23: shows Total Sessions, Sessions per day, Sessions per child and heatmap', () => {
    render(<PixelbotSummaryView />)
    expect(screen.getByText('Total Sessions')).toBeInTheDocument()
    expect(screen.getByText('Sessions per day')).toBeInTheDocument()
    expect(screen.getByText('Sessions per child')).toBeInTheDocument()
    expect(screen.getByText('42')).toBeInTheDocument()
    expect(screen.getByText('4')).toBeInTheDocument()
    expect(document.getElementById('summary-heatmap')).toBeInTheDocument()
  })

  it('shows Loading when isLoading is true', () => {
    usePixelbotSummary.mockReturnValue({ summaryStats: null, isLoading: true })
    render(<PixelbotSummaryView />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })
})
