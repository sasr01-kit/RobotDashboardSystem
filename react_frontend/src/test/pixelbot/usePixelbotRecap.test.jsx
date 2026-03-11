import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { usePixelbotRecap } from '../../modules/pixelbot/hooks/usePixelbotRecap'
import { mockRecapResponse } from '../../modules/pixelbot/__mocks__/data'

// Tests for usePixelbotRecap to ensure it fetches recap data correctly, handles loading and error states,
// and maps the response to the expected format
describe('usePixelbotRecap', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockRecapResponse),
        })
      )
    )
  })

  it('fetches /pixelbot/children/:childId/recap and returns child recap (T27)', async () => {
    const { result } = renderHook(() => usePixelbotRecap('c1'))

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(fetch).toHaveBeenCalledWith('http://localhost:8080/pixelbot/children/c1/recap')
    expect(result.current.child).toBeDefined()
    expect(result.current.child.name).toBe('Child One')
    expect(result.current.child.metricValues.totalSessions).toBe(2)
    expect(result.current.child.sessionFrequencyData).toBeDefined()
    expect(result.current.child.metricValues.sessionTrendPercentage).toBe('100.0')
  })

  it('does not fetch when childId is missing', async () => {
    const { result } = renderHook(() => usePixelbotRecap(null))

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(fetch).not.toHaveBeenCalled()
    expect(result.current.child).toBeNull()
  })

  it('maps drawings array into base64 data URLs when drawings are present', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              ...mockRecapResponse,
              drawing: {
                ...mockRecapResponse.drawing,
                drawings: [{ base64: 'abc123' }, { base64: 'def456' }],
              },
            }),
        })
      )
    )

    const { result } = renderHook(() => usePixelbotRecap('c1'))

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.child.drawings).toEqual([
      'data:image/png;base64,abc123',
      'data:image/png;base64,def456',
    ])
  })

  it('keeps trend at 0.0 when previous month count is zero', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              ...mockRecapResponse,
              engagement: {
                ...mockRecapResponse.engagement,
                sessionFrequencyTrend: [
                  { month: 'Jan', count: 0 },
                  { month: 'Feb', count: 3 },
                ],
              },
            }),
        })
      )
    )

    const { result } = renderHook(() => usePixelbotRecap('c1'))

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.child.metricValues.sessionTrendPercentage).toBe('0.0')
  })

  it('uses default fallbacks when optional backend sections are missing', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              name: 'Fallback Child',
              engagement: {
                totalSessions: 0,
              },
            }),
        })
      )
    )

    const { result } = renderHook(() => usePixelbotRecap('c1'))

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.child.name).toBe('Fallback Child')
    expect(result.current.child.sessionFrequencyData).toEqual([])
    expect(result.current.child.wordCountData).toEqual([])
    expect(result.current.child.speechTimeData).toEqual([])
    expect(result.current.child.intimacyScoreData).toEqual([])
    expect(result.current.child.drawings).toEqual([])

    expect(result.current.child.metricValues).toMatchObject({
      totalSessions: 0,
      sessionTrendPercentage: '0.0',
      totalWordCount: 0,
      averageWordCount: 0,
      averageIntimacyScore: 0,
      averageStrokeCount: 0,
      averageNumberColors: 0,
      averageFilledArea: 0,
      averageNumberObjects: 0,
      mostCommonObjects: [],
      objectDiversity: 0,
    })
  })

  it('sets error when fetch fails', async () => {
    vi.stubGlobal('fetch', vi.fn(() => Promise.reject(new Error('Network error'))))
    vi.spyOn(console, 'error').mockImplementation(() => {})

    const { result } = renderHook(() => usePixelbotRecap('c1'))

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.error).toBe('Failed to load data.')
    expect(result.current.child).toBeNull()
  })

  it('sets error when response is not ok', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() => Promise.resolve({ ok: false, json: () => Promise.resolve({}) }))
    )
    vi.spyOn(console, 'error').mockImplementation(() => {})

    const { result } = renderHook(() => usePixelbotRecap('c1'))

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.error).toBe('Failed to load data.')
  })
})
