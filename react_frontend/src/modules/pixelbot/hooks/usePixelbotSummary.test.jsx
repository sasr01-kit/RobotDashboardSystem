import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { usePixelbotSummary } from './usePixelbotSummary'
import { mockSummaryResponse } from '../__mocks__/data'

describe('usePixelbotSummary', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockSummaryResponse),
        })
      )
    )
  })

  it('fetches /pixelbot/summary and maps to summaryStats (T20, T23)', async () => {
    const { result } = renderHook(() => usePixelbotSummary())

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(fetch).toHaveBeenCalledWith('http://localhost:8080/pixelbot/summary')
    expect(result.current.summaryStats).toBeDefined()
    expect(result.current.summaryStats.totalSessions).toBe(42)
    expect(result.current.summaryStats.avgSessionsPerChild).toBe(4)
    expect(result.current.summaryStats.sessionsPerDay).toBe(2)
    expect(result.current.summaryStats.dailySessionCounts).toBeDefined()
    expect(result.current.summaryStats.colorScale).toEqual([])
  })

  it('T26: fetches only from backend (localhost:8080), no external URLs', async () => {
    renderHook(() => usePixelbotSummary())
    await waitFor(() => {
      expect(fetch).toHaveBeenCalled()
    })
    expect(fetch).toHaveBeenCalledTimes(1)
    expect(fetch).toHaveBeenCalledWith(expect.stringContaining('http://localhost:8080/pixelbot/'))
  })
})
