import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { usePixelbotSummary } from '../../modules/pixelbot/hooks/usePixelbotSummary'
import { mockSummaryResponse } from '../../modules/pixelbot/__mocks__/data'

// Tests for usePixelbotSummary to ensure it fetches summary data correctly, handles loading and error states,
// and maps the response to the expected format
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

  it('sets error when fetch fails', async () => {
    vi.stubGlobal('fetch', vi.fn(() => Promise.reject(new Error('Network error'))))
    vi.spyOn(console, 'error').mockImplementation(() => {})

    const { result } = renderHook(() => usePixelbotSummary())

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.error).toBe('Failed to fetch summary stats')
    expect(result.current.summaryStats).toBeNull()
  })

  it('returns empty heatmap data when dailySessionCounts is empty', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              ...mockSummaryResponse,
              dailySessionCounts: {},
            }),
        })
      )
    )

    const { result } = renderHook(() => usePixelbotSummary())

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.summaryStats.dailySessionCounts).toEqual([])
  })

  it('maps Sunday and Monday correctly when first entry is Sunday', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              ...mockSummaryResponse,
              dailySessionCounts: {
                '2-3-2025': 5,
                '3-3-2025': 7,
              },
            }),
        })
      )
    )

    const { result } = renderHook(() => usePixelbotSummary())

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    const points = result.current.summaryStats.dailySessionCounts

    expect(points[0].value).toBe(5)
    expect(points[0].x).toBe(0)
    expect(points[0].y).toBe(6)

    expect(points[1].value).toBe(7)
    expect(points[1].x).toBe(1)
    expect(points[1].y).toBe(0)
  })

  it('handles missing colorScale fallback branch by surfacing an error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              ...mockSummaryResponse,
              colorScale: null,
            }),
        })
      )
    )
    vi.spyOn(console, 'error').mockImplementation(() => {})

    const { result } = renderHook(() => usePixelbotSummary())

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.error).toBe('Failed to fetch summary stats')
    expect(result.current.summaryStats).toBeNull()
  })
})
