import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { usePixelbotRecap } from './usePixelbotRecap'
import { mockRecapResponse } from '../__mocks__/data'

describe('usePixelbotRecap', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn((url) =>
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
  })

  it('does not fetch when childId is missing', async () => {
    const { result } = renderHook(() => usePixelbotRecap(null))
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })
    expect(fetch).not.toHaveBeenCalled()
    expect(result.current.child).toBeNull()
  })
})
